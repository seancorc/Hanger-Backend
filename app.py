import json
import config
import random
from flask import Flask, request
from UserAPI import userAPI
from db import db, User, Post, ImageURL
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from sqlalchemy.sql.expression import and_
from geoalchemy2 import func, WKTElement

app = Flask(__name__)
app.register_blueprint(userAPI)

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
                        lat = 33.80019 + i/1000
                        longt = -118.390442 + i/1000
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
                        post = Post(clothingType=clothingType, category=category, 
                        name=test, brand=test, price=i, description=test, userID=i)
                        lat = 33.80019 + i/1000
                        longt = -118.390442 + i/1000
                        post.point = WKTElement('POINT({} {})'.format(longt, lat), srid=4326)
                        db.session.add(post)
                        db.session.add(ImageURL(url='https://picsum.photos/id/500', postID=post.id))
                db.session.commit()
#populatePost()

@jwt.unauthorized_loader
def noAccessToken(callback):
        return json.dumps({'error': 'Unauthorized Access Token'}), 401

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    return json.dumps({'error': 'Expired Access Token'}), 401
        

@app.route('/api/post/create/', methods=['POST'])
@jwt_required
def createPost(): #TODO: ADD Custom Point When Post Is Created
        userID = get_jwt_identity()
        postBody = json.loads(request.data)
        clothingType = postBody['clothingType']
        category = postBody['category']
        name = postBody['name']
        brand = postBody['brand']
        price = postBody['price']
        description = postBody['description']
        imageURLs = postBody['imageURLs']
        post = Post(clothingType=clothingType, category=category, name=name, 
        brand=brand, price=price, description=description, userID=userID)
        user = User.query.get(userID)
        post.point = user.point
        db.session.add(post)
        db.session.commit()
        for url in imageURLs:
                imageURL = ImageURL(url=url, postID=post.id)
                db.session.add(imageURL)
        db.session.commit()
        res = {'data': post.serialize()}
        return json.dumps(res), 201

@app.route('/api/posts/', methods=['GET'])
@jwt_required
def getPosts():
        #NOTE: POSTGIS COORDS ARE (LONG, LAT)
        minPrice = request.args.get('minPrice')
        maxPrice = request.args.get('maxPrice')
        radius = request.args.get('radius')
        clothingTypes = request.args.get('type')
        categories = request.args.get('category')
        userID = get_jwt_identity()
        user = User.query.filter_by(id=userID).first()
        query = Post.query.filter(Post.userID != userID)
        if not minPrice is None:
                minPrice = int(minPrice)
                query.filter(Post.price >= minPrice)
        if not maxPrice is None:
                maxPrice = int(maxPrice)
                query.filter(Post.price <= maxPrice)
        if not radius is None:
                radius = float(radius) * 1609.34 #Converting to meters
                query.filter(func.ST_DistanceSphere(Post.point, user.point) <= radius) 
        if not clothingTypes is None:
                clothingTypes = json.loads(clothingTypes)
                for ct in clothingTypes:
                        query.filter(Post.clothingType == ct)
        if not categories is None:
                categories = json.loads(categories)
                for cat in categories:
                        query.filter(Post.category == categories)
        posts = query.all()
        random.shuffle(posts)
        res = {'data': [post.serialize() for post in posts]}
        return json.dumps(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
