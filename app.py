import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.event import Event, EventList
from resources.story import Story, StoryList

app = Flask(__name__)
app.secret_key = "$am3+Pag3+K3y"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Event, "/event/<name>")
api.add_resource(EventList, "/events")
api.add_resource(Story, "/story/<name>")
api.add_resource(StoryList, "/stories")
api.add_resource(EventStoryList, "/stories/<name>")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
