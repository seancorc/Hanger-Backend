from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context #Note: passlib hash functions automatically handle salting

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    profilePictureURL = db.Column(db.String, nullable=True)
    posts = db.relationship('Post', back_populates='user')

    def __init__(self, **kwargs):
        self.email = kwargs.get('email', '')
        self.username = kwargs.get('username', '')

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'profilePictureURL': self.profilePictureURL,
            'posts': [post.subSerialize() for post in self.posts]
        }

    def subSerialize(self):
        return {
        'id': self.id,
        'email': self.email,
        'username': self.username,
        'profilePictureURL': self.profilePictureURL
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
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    imageURLS = db.relationship('ImageURL', back_populates='post')
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='posts')

    def __init__(self, **kwargs):
        self.clothingType = kwargs.get('clothingType', '')
        self.category = kwargs.get('category', '')
        self.name = kwargs.get('name', '')
        self.brand = kwargs.get('brand', '')
        self.price = kwargs.get('price', '')
        self.description = kwargs.get('description', '')
        self.userID = kwargs.get('userID', '')

    def serialize(self):
        return {
            'id': self.id,
            'category': self.category,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'description': self.description,
            'user': self.user.subSerialize()
        }
        
    def subSerialize(self):
        return {
            'id': self.id,
            'category': self.category,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'description': self.description
        }


class ImageURL(db.Model):
    __tablename__ = 'imageURL'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    post = db.relationship('Post', back_populates='imageURLS')
    postID = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', '')
        self.postID = kwargs.get('postID')