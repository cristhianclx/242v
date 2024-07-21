from flask import Flask, render_template
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_socketio import SocketIO


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'cibertec2024'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"

socketio = SocketIO(app)

ma = Marshmallow(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    importance = db.Column(db.Text, nullable=True, default="low")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Message {self.id}>"
    

@app.route("/")
def index():
    messages = Message.query.all()
    return render_template("index.html", messages = messages)


@socketio.on('welcome')
def handle_welcome(data):
    print('received data on welcome: ' + str(data))


@socketio.on('messages')
def handle_messages(data):
    print('received data on messages: ' + str(data))
    message = Message(**data)
    db.session.add(message)
    db.session.commit()
    socketio.emit("messages-responses", data)