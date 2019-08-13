import json
import config
from flask import Flask, request
from UserAPI import userAPI
from db import db, User, Post, ImageURL
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from geoalchemy2 import func, WKTElement

app = Flask(__name__)
app.register_blueprint(userAPI)

#TODO: Move from sqlite to PostgreSQL 
#db_filename = 'Testing.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
jwt = JWTManager(app)

db.init_app(app)
with app.app_context():
        db.create_all()

def populateUser():
        with app.app_context():
                for i in range(1, 100):
                        email = "Test{}@Test.com".format(i)
                        username = "TestUser{}".format(i)
                        password = "TestPass{}".format(i)
                        user = User(email=email, username=username)
                        user.passwordHash = password
                        longt = 118.2437 + i/1000
                        lat = 34.0522 + i/1000
                        user.point = WKTElement('POINT({} {})'.format(longt, lat), srid=4326)
                        db.session.add(user)
                db.session.commit()

#populateUser()

def populatePost():
        with app.app_context():
                for i in range(1, 100):
                        clothingType = "Male"
                        category = "Workout"
                        test = "Test{}".format(i)
                        post = Post(clothingType=clothingType, category=category, name=test, brand=test, price=i, description=test, userID=i)
                        longt = 118.2437 + i/1000
                        lat = 34.0522 + i/1000
                        post.point = WKTElement('POINT({} {})'.format(longt, lat), srid=4326)
                        db.session.add(post)
                db.session.commit()
#populatePost()

#TODO Learn blueprints and split up python file
@jwt.unauthorized_loader
def noAccessToken(callback):
        return json.dumps({'error': 'Unauthorized Access Token'}), 401

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    return json.dumps({'error': 'Expired Access Token'}), 401
        
        
@app.route('/api/posts/', methods=['GET']) #For Development Only
def getAllPosts():
     allPost = Post.query.all() 
     res = {'data': [post.serialize() for post in allPost]}
     print(res)
     return json.dumps(res), 200

@app.route('/api/post/create/', methods=['POST'])
@jwt_required
def createPost(): #TODO: ADD POINT WHEN POST IS CREATED
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
        return json.dumps(res), 201

@app.route('/api/posts/nearby', methods=['GET'])
@jwt_required
def getNearbyPosts():
        #NOTE: POSTGIS COORDS ARE (LONG, LAT)
        statuscode = 500
        print(request.args)
        radius = float(request.args.get('radius'))
        userID = get_jwt_identity()
        user = User.query.filter_by(id=userID).first()
        if user is None:
                res = {'error': "User Does Not Exist"} 
                statuscode = 400
        else:   
                radius = radius * 1609.34 #Converting to meters
                nearbyPosts = Post.query.filter(func.ST_DistanceSphere(Post.point, user.point) <= radius)
                res = {'data': [post.serialize() for post in nearbyPosts]}
                statuscode = 200
        return json.dumps(res), statuscode



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
