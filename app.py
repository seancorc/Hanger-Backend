import json
import config
from flask import Flask, request
from db import db, User, Post, ImageURL
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)

#TODO: Move from sqlite to PostgreSQL 
db_filename = 'Testing.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
jwt = JWTManager(app)

db.init_app(app)
with app.app_context():
        db.create_all()


#TODO Learn blueprints and split up python file
@jwt.unauthorized_loader
def noAccessToken(callback):
        return json.dumps({'error': 'Unauthorized Access'}), 401

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    return json.dumps({'error': 'Expired Access'}), 401
        

@app.route('/api/user/signup/', methods=['POST'])
def createUser():
        statuscode = 500
        postBody = json.loads(request.data)
        email = postBody['email']
        password = postBody['password']
        username = postBody['username']
        possibleUserWithEmail = User.query.filter_by(email=email).first()
        possibleUserWithUsername = User.query.filter_by(username=username).first()
        if not (possibleUserWithEmail is None):
                res = {'error': "User with that email already exists"}
                statuscode = 401
        elif not (possibleUserWithUsername is None):
                res = {'error': "User with that username already exists"}
                statuscode = 401
        else:
                user = User(email = email, username = username)
                user.hashAndSetPassword(password)
                db.session.add(user)
                db.session.commit()
                accessToken = create_access_token(identity=user.id, expires_delta=False) #implement expires functionality at some point
                res = {'data': user.serialize(), 'accessToken': accessToken}
                statuscode = 201
        return json.dumps(res), statuscode

@app.route('/api/user/login/', methods=['POST'])
def login():
        statuscode = 500
        postBody = json.loads(request.data)
        email = postBody['email']
        password = postBody['password']
        user = User.query.filter_by(email=email).first()
        if user is None:
                res = {'error': "Incorrect Email"} 
                statuscode = 400
        elif not user.verifyPassword(password):
                res = {'error': 'Incorrect Password'}
                statuscode = 400
        else: 
                accessToken = create_access_token(identity=user.id, expires_delta=False) #implement expires functionality at some point
                res = {'data': user.serialize(), 'accessToken': accessToken}
                statuscode = 200
        return json.dumps(res), statuscode

@app.route('/api/user/updateinfo/', methods=['PUT'])
@jwt_required
def updateUserInfo():
        statuscode = 500
        userID = get_jwt_identity()
        user = User.query.filter_by(id=userID).first()
        if user is None:
                res = {'error': "User does not exist"}
                statuscode = 400
        else:
                postBody = json.loads(request.data)
                newEmail = postBody['newEmail']
                newUsername = postBody['newUsername']
                user.email = newEmail
                user.username = newUsername
                db.session.commit()
                statuscode = 200
                res = {'data': user.serialize()}
        return json.dumps(res), statuscode

@app.route('/api/user/updatepassword/', methods=['PUT'])
@jwt_required
def updatePassword():
        statuscode = 500
        userID = get_jwt_identity()
        user = User.query.filter_by(id=userID).first()
        if user is None:
                res = {'error': "User does not exist"}
                statuscode = 400
        else:
                postBody = json.loads(request.data)
                currentPassword = postBody['currentPassword']
                newPassword = postBody['newPassword']
                if not user.verifyPassword(currentPassword):
                        res = {'error': "Incorrect Password"}
                        statuscode = 400
                else:
                        user.hashAndSetPassword(newPassword)
                        db.session.commit()
                        res = {'success': True}
                        statuscode = 200
        return json.dumps(res), statuscode

@app.route('/api/user/profilepicture/', methods=['PUT'])
@jwt_required
def modifyProfilepicture():
        statuscode = 500
        userID = get_jwt_identity()
        user = User.query.filter_by(id=userID).first()
        if user is None:
                res = {'error': "User does not exist"}
                statuscode = 400
        else:
                postBody = json.loads(request.data)
                url = postBody['url']
                user.profilePictureURL = url
                db.session.commit()
                res = {'success': True}
                statuscode = 200
        return json.dumps(res), statuscode
        

@app.route('/api/users/', methods=['GET']) #For Development Only
def getAllUsers():
    allUsers = User.query.all()
    res = {'data': [
        user.serialize() for user in allUsers]}
    return json.dumps(res), 200

@app.route('/api/post/create/', methods=['POST'])
@jwt_required
def createPost():
        userID = get_jwt_identity()
        postBody = json.loads(request.data)
        clothingType = postBody['clothingType']
        category = postBody['category']
        name = postBody['name']
        brand = postBody['brand']
        price = postBody['price']
        description = postBody['description']
        imageURLs = postBody['imageURLs']
        post = Post(clothingType=clothingType, category=category, name=name, brand=brand, price=price, description=description, userID=userID)
        db.session.add(post)
        db.session.commit()
        for url in imageURLs:
                imageURL = ImageURL(url=url, postID=post.id)
                db.session.add(imageURL)
        db.session.commit()
        res = {'data': post.serialize()}
        print(res)
        return json.dumps(res), 201

@app.route('/api/user/posts/', methods=['GET'])
@jwt_required
def getPostsForUser():
        statuscode = 500
        userID = get_jwt_identity()
        user = User.query.filter_by(id=userID).first()
        if user is None:
                res = {'error': "User does not exist"}
                statuscode = 400
        else:
                res = {'data': [post.subSerialize() for post in user.posts]}
                statuscode = 200
        return json.dumps(res), statuscode
        
@app.route('/api/posts/', methods=['GET']) #For Development Only
def getAllPosts():
     allPost = Post.query.all()
     res = {'data': [post.serialize() for post in allPost]}
     return json.dumps(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
