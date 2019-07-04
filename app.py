import json
from flask import Flask, request
from db import db, User


app = Flask(__name__)

db_filename = 'todo.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
        db.create_all()


@app.route('/helloworld')
def helloworld():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
