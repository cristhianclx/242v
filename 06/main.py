from flask import Flask
from flask_restful import Resource, Api
import requests


app = Flask(__name__)
api = Api(app)


class IndexResource(Resource):
    def get(self):
        return {}, 204


class PingResource(Resource):
    def get(self):
        return {
            "response": "PONG"
        }


class PokemonResource(Resource):
    def get(self, name):
        raw = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name))
        if raw.ok:
            data = raw.json()
            print(data)
            return {
                "name": name,
                "height": data["height"],
                # weight
                # abilities ["static", "lightning-pod"]
                # forms ["pikachu"]
            }
        else:
            return {
                "error": "ERROR"
            }, 400


api.add_resource(IndexResource, "/")
api.add_resource(PingResource, "/ping")
api.add_resource(PokemonResource, "/pokemon/<name>")


if __name__ == "__main__":
    app.run(debug = True)