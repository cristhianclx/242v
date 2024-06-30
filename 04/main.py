from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sistemas@127.0.0.1:5432/cibertec'
# https://docs.sqlalchemy.org/en/20/core/engines.html

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    country = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User {}>".format(self.id)


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
                       
    def __repr__(self):
        return "<Message {}>".format(self.id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def users():
    users_data = User.query.all()
    return render_template("users.html", users=users_data)


@app.route("/users/add", methods=["GET", "POST"])
def users_add():
    if request.method == "GET":
        return render_template("users-add.html")
    if request.method == "POST":
        user = User(id = request.form["id"], first_name=request.form["first_name"], last_name=request.form["last_name"], age=request.form["age"], country=request.form["country"])
        db.session.add(user)
        db.session.commit()
        return render_template("users-add.html", message="User added")


@app.route("/users/<id>")
def users_by_id(id):
    user = User.query.get_or_404(id)
    return render_template("users-detail.html", user=user)


@app.route("/users/edit/<id>", methods=["GET", "POST"])
def users_edit_by_id(id):
    user = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-edit.html", user=user)
    if request.method == "POST":
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.age = request.form["age"]
        user.country = request.form["country"]
        db.session.add(user)
        db.session.commit()
        return render_template("users-edit.html", user=user, message="User edited")


@app.route("/users/delete/<id>", methods=["GET", "POST"])
def users_delete_by_id(id):
    user = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-delete.html", user=user)
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users'))