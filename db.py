from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password
        }
