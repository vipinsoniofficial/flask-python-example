from flask_marshmallow import Marshmallow
from marshmallow import fields
from server import app, logging
from config import db
import datetime as dt

from flask_sqlalchemy import SQLAlchemy
# from server import app, logging

ma = Marshmallow(app)

# static
_id = 101


class User(db.Model):
    logging.info("In Class User of main_model.py")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    # created_at = db.Column(db.date)

    def __init__(self, username, email):
        logging.info("In __init__ of Class User of main_model.py")
        global _id
        self.id = _id
        self.username = username
        self.email = email
        # self.create_at = dt.datetime.now()
        _id += 1
        logging.info("Going Out of __init__ of Class User of main_model.py")

    def __repr__(self):
        logging.info("In __repr__ of Class User of main_model.py")
        return {"id": self.id,
                "username": self.username,
                "email": self.email}
        # , "created_at": self.create_at}


class UserSchema(ma.Schema):
    logging.info("In Class UserSchema of main_model.py")

    class Meta:
        fields = ('id', 'username', 'email', 'created_at')
        logging.info("In Class Meta of Class UserSchema of main_model.py")

    username = fields.String()
    email = fields.String()


user_schema = UserSchema()
users_schema = UserSchema(many=True)



'''
logging.info("In config.py: database Configuration")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
'''