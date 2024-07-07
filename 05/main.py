from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    routine_id = db.Column(db.Integer, nullable=True)
    show_id = db.Column(db.Integer, nullable=True)
    event_name = db.Column(db.String(255), nullable=True)
    show_name = db.Column(db.String(255), nullable=True)
    start_timestamp = db.Column(db.String(8), nullable=True)
    text = db.Column(db.Text)
    video_id = db.Column(db.String(20))

    def __repr__(self):
        return "<Joke {}>".format(self.id)


@app.route("/")
def index():
    jokes = Joke.query.all()
    return render_template("index.html", jokes=jokes)