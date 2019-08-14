from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry, func, shape

from passlib.apps import custom_app_context as pwd_context #Note: passlib hash functions automatically handle salting

db = SQLAlchemy()

def __getLongtFromText__(text):
    '''
    Slices result of shape.to_shape(Point).to_wkt() and returns the longtitude as a float
    (If there is an error while slicing or casting returns None)
    '''
    try:
        firstparenindex = text.index('(')
        spaceindex = text.rindex(' ')
        lat = text[firstparenindex + 1:spaceindex]
        return float(lat)
    except:
        return None

def __getLatFromText__(text):
    '''
    Slices result of shape.to_shape(Point).to_wkt() and returns the latitude as a float
    (If there is an error while slicing or casting returns None)
    '''
    try:
        spaceindex = text.rindex(' ')
        lastparen = text.rindex(')')
        longt = text[spaceindex + 1 : lastparen]
        return float(longt)
    except:
        return None

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    profilePictureURL = db.Column(db.String, nullable=True)
    posts = db.relationship('Post', back_populates='user')
    point = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email', '')
        self.username = kwargs.get('username', '')

    def serialize(self):
        try:
            text = shape.to_shape(self.point).to_wkt() #Turns point into a string 
        except:
            text = None
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'profilePictureURL': self.profilePictureURL,
            'posts': [post.subSerialize() for post in self.posts],
            'lat':  __getLatFromText__(text=text),
            'longt': __getLongtFromText__(text=text)
            }


    def subSerialize(self):
        try:
            text = shape.to_shape(self.point).to_wkt() #Turns point into a string 
        except:
            text = None
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'profilePictureURL': self.profilePictureURL,
            'lat':  __getLatFromText__(text),
            'longt': __getLongtFromText__(text)
            }

    def hashAndSetPassword(self, password):
        self.passwordHash = pwd_context.hash(password)

    def verifyPassword(self, password):
        return pwd_context.verify(password, self.passwordHash)

    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    clothingType = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    imageURLs = db.relationship('ImageURL', back_populates='post')
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='posts')
    point = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    def __init__(self, **kwargs):
        self.clothingType = kwargs.get('clothingType', '')
        self.category = kwargs.get('category', '')
        self.name = kwargs.get('name', '')
        self.brand = kwargs.get('brand', '')
        self.price = kwargs.get('price', '')
        self.description = kwargs.get('description', '')
        self.userID = kwargs.get('userID', '')

    def serialize(self):
        try:
            text = shape.to_shape(self.point).to_wkt() #Turns point into a string 
        except:
            text = None
        return {
            'id': self.id,
            'clothingType': self.clothingType,
            'category': self.category,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'description': self.description,
            'user': self.user.subSerialize(),
            'imageURLs': [imageURL.urlString() for imageURL in self.imageURLs],
            'lat':  __getLatFromText__(text),
            'longt': __getLongtFromText__(text) 
        }
        
    def subSerialize(self):
        try:
            text = shape.to_shape(self.point).to_wkt() #Turns point into a string 
        except:
            text = None
        return {
            'id': self.id,
            'clothingType': self.clothingType,
            'category': self.category,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'description': self.description,
            'imageURLs': [imageURL.urlString() for imageURL in self.imageURLs],
            'lat':  __getLatFromText__(text),
            'longt': __getLongtFromText__(text) 
        }


class ImageURL(db.Model):
    __tablename__ = 'imageURL'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    post = db.relationship('Post', back_populates='imageURLs')
    postID = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', '')
        self.postID = kwargs.get('postID')

    def urlString(self):
        return self.url