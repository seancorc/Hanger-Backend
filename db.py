from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')
        self.username = kwargs.get('username', '')
        self.latitude = kwargs.get('latitude', '')
        self.longitude = kwargs.get('longitude', '')

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'latitude': self.latitude,
            'longitutde': self.longitude
        }

    

    
