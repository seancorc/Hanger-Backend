import json
from flask import Flask, request
from db import db, User


app = Flask(__name__)

#TODO: Move from sqlite to PostgreSQL 
db_filename = 'Testing.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
        db.create_all()


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
                res = {'data': user.serialize()}
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
                res = {'data': user.serialize()}
                statuscode = 200
        return json.dumps(res), statuscode

@app.route('/api/user/updateinfo/', methods=['PUT'])
def updateUserInfo():
        statuscode = 500
        postBody = json.loads(request.data)
        userID = postBody['userID']
        newEmail = postBody['newEmail']
        newUsername = postBody['newUsername']
        user = User.query.filter_by(id=userID).first()
        if user is None:
                res = {'error': "User does not exist"}
                statuscode = 400
        else:
                user.email = newEmail
                user.username = newUsername
                db.session.commit()
                statuscode = 200
                res = {'data': user.serialize()}
        return json.dumps(res), statuscode

@app.route('/api/users/', methods=['GET']) #For Development Only
def getAllUsers():
    allUsers = User.query.all()
    res = {'data': [
        user.serialize() for user in allUsers]}
    return json.dumps(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
