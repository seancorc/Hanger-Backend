from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context #Note: passlib hash functions automatically handle salting

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    posts = relationship('post', back_populates='user')

    def __init__(self, **kwargs):
        self.email = kwargs.get('email', '')
        self.username = kwargs.get('username', '')

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
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
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))

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
            'userID': self.userID
        }
        




    
