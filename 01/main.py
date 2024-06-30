from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, Cibertec!</p>"

@app.route("/data")
def data():
    return "<p>Example of DATA</p>"

@app.route("/messages")
def messages():
    return [{
        "id": 1,
        "content": "A message"
    }, {
        "id": 2,
        "content": "Another message"
    }]

@app.route("/messages/<int:id>")
def messages_by_id(id):
    return {
        "id": id,
        "content": "Another message"
    }


data = [{
    "user": "raul",
    "password": 123456
}, {
    "user": "cristhian",
    "password": 123456
}, {
    "user": "frank",
    "password": 12345678
}]

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return "you need to login"
    if request.method == "POST":
        raw = request.get_json()
        print(raw)
        user = raw.get("user")
        password = raw.get("password")
        # verificar con la data del array
        # si es valido devolver "valid login"
        # si es invalido devolver "invalid login"
        return "login"

# /login
# {"user": "cristhian", "password": "123456"}

# GET /login?user=cristhian&password=123456
# POST /login
# {user:cristhian, password:123456}