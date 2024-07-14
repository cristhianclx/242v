from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User {}>".format(self.id)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message {}>".format(self.id)

    
class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "age",
            "content",
            "created_at",
        )
        model = User
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_schema = UserSchema()
users_schema = UserSchema(many = True)


class UserPublicSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
        )
        model = User
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_public_schema = UserPublicSchema()
users_public_schema = UserPublicSchema(many = True)


class IndexResource(Resource):
    def get(self):
        return {
            "working": True,
        }


class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


class UserIDResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user_schema.dump(user)
    
    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        user.name = data.get("name", user.name)
        user.age = data.get("age", user.age)
        user.content = data.get("content", user.content)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)
    
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204


class UsersPublicResource(Resource):
    def get(self):
        users = User.query.all()
        return users_public_schema.dump(users)


api.add_resource(IndexResource, "/")
api.add_resource(UsersPublicResource, "/users-public/")
api.add_resource(UsersResource, "/users")
api.add_resource(UserIDResource, "/users/<int:id>")

# /messages
#  ( ) GET - 200: read all messages
#  ( ) POST - 201: create message
# /messages/1
#  ( ) GET - 200: read one
#  ( ) DELETE - 204: delete
# /messages-by-user/<user_id>
#  ( ) GET - 200: messages by user