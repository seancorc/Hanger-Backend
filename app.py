import json
from flask import Flask, request
from db import db, User
from sqlalchemy import or_


app = Flask(__name__)

db_filename = 'Hung.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
        db.create_all()


@app.route('/helloworld/')
def helloworld():
        return "Hello World!"

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
                res = {'success': False, 'error': "User with that email already exists"}
                statuscode = 401
        elif not (possibleUserWithUsername is None):
                res = {'success': False, 'error': "User with that username already exists"}
                statuscode = 402
        else:
                user = User(email = email, password = password, username = username)
                db.session.add(user)
                db.session.commit()
                res = {'success': True, 'data': user.serialize()}
                statuscode = 201
        return json.dumps(res), statuscode

@app.route('/api/user/login/', methods=['POST'])
def login():
        statuscode = 500
        postBody = json.loads(request.data)
        email = postBody['email']
        password = postBody['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
                res = {'success': False, 'error': "User not found"} 
                statuscode = 400 
        else: 
                res = {'success': True, 'data': user.serialize()}
                statuscode = 200
        return json.dumps(res), statuscode

@app.route('/api/user/updateinfo/', methods=['POST'])
def updateUserInfo():
        postBody = json.loads(request.data)
        previousEmail = postBody['previousEmail']
        newEmail = postBody['newEmail']
        previousUsername = postBody['previousUsername']
        newUsername = postBody['newUsername']
        user = User.query.filter_by(email=previousEmail, username=previousUsername).first()
        if user is None:
                res = {'success': False, 'error': "User does not exist"}
        else:
                user.email = newEmail
                user.username = newUsername
                db.session.commit()
                res = {'success': True, 'data': user.serialize()}
        return json.dumps(res), 200 if res['success'] else 400


@app.route('/api/users/')
def getAllUsers():
    allUsers = User.query.all()
    res = {'success': True, 'data': [
        user.serialize() for user in allUsers]}
    return json.dumps(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
