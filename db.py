from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context #Note: passlib hash functions automatically handle salting

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)

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

    

    
