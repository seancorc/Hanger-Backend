from flask import Blueprint, request
import json
from db import db, User
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import geoalchemy2

userAPI = Blueprint('userAPI', __name__)

@userAPI.route('/api/user/signup/', methods=['POST'])
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
                user = User(email=email, username=username) #Default lat long are LA
                user.hashAndSetPassword(password)
                user.point = geoalchemy2.WKTElement('POINT(5 45)', srid=4326)
                db.session.add(user)
                db.session.commit()
                accessToken = create_access_token(identity=user.id, expires_delta=False) #implement expires functionality at some point
                res = {'data': user.serialize(), 'accessToken': accessToken}
                statuscode = 201
        return json.dumps(res), statuscode

@userAPI.route('/api/user/login/', methods=['POST'])
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

@userAPI.route('/api/user/location/', methods=['PUT'])
@jwt_required
def updateUserLocation():
    statuscode = 500
    user = User.query.filter_by(email=email).first()
    if user is None:
            res = {'error': "Incorrect Email"} 
            statuscode = 400
    else: 
        postBody = json.loads(request.data)
        lat = postBody['lat']
        longt = postBody['longt']
        user.lat = lat
        user.longt = longt
        db.session.commit()
        statuscode = 200
        res = {'data': user.serialize()}
    return json.dumps(res), statuscode


@userAPI.route('/api/user/updateinfo/', methods=['PUT'])
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

@userAPI.route('/api/user/updatepassword/', methods=['PUT'])
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

@userAPI.route('/api/user/profilepicture/', methods=['PUT'])
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

@userAPI.route('/api/user/posts/', methods=['GET'])
@jwt_required
def getPostsForUser():
        statuscode = 500
        userID = get_jwt_identity()
        user = User.query.filter_by(id=userID).first()
        if user is None:
                res = {'error': "User does not exist"}
                statuscode = 400
        else:
                res = {'data': [post.serialize() for post in user.posts]}
                statuscode = 200
        return json.dumps(res), statuscode


@userAPI.route('/api/users/', methods=['GET']) #For Development Only
def getAllUsers():
    allUsers = User.query.all()
    res = {'data': [
        user.serialize() for user in allUsers]}
    return json.dumps(res), 200