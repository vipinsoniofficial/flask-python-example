from flask import Flask
from flask_marshmallow import Marshmallow
from your_orm import Model, Column, Integer, String , DateTime


app = Flask(__name__)
ma = Marshmallow(app)


# write you models
class User(Model):
    email = Column(String)
    password = Column(String)
    date_created = Column(DateTime, auto_now_add=True)


# Defining output format with marshmallow
class UserSchema(ma.Schema):
    # fields to expose
    fields = ("email", "date_created", "_links")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {"self": ma.URLFOR("user_details", id="<id>"), "collection": ma.URLFOR("users")}
        )


user_schema = UserSchema()
users_schema= UserSchema(many=True)


# Output the data in your views
@app.route("/api/users/")
def users():
    all_users = User.all()
    return users_schema.dump(all_users)


@app.route("/api/users/<id>")
def user_detail(id):
    user = User.get(id)
    return users_schema.dump(user)

