import json
from flask import Flask, request
from db import db, User


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

@app.route('/api/user/', methods=['POST'])
def createUser():
        postBody = json.loads(request.data)
        email = postBody['email']
        password = postBody['password']
        username = postBody['username']
        latitude = postBody['latitude']
        longitude = postBody['longitude']
        user = User(email = email, password = password, username = username, latitude = latitude, longitude = longitude)
        db.session.add(user)
        db.session.commit()
        res = {'success': True, 'data': user.serialize()}
        return json.dumps(res), 201

@app.route('/api/users/')
def getAllUsers():
    allUsers = User.query.all()
    res = {'success': True, 'data': [
        user.serialize() for user in allUsers]}
    return json.dumps(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
