import sqlite3
from flask import request
from flask_restful import Resource
from models.user import UserModel
from schemas.user import UserSchema
from marshmallow import ValidationError

HELP_TEXT = "Field required."
CREATED = "User created succesfully."

user_schema = UserSchema()

class UserRegister(Resource):

    @classmethod
    def post(cls):
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        if UserModel.find_by_username(user.username):
            return {"message": f"User {data['username']} already exists."}, 400

        user.save_to_db()
        return {"message": CREATED}, 201
