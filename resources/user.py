import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

HELP_TEXT = "Field required."
CREATED = "User created succesfully."

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help=HELP_TEXT)
    parser.add_argument("password", type=str, required=True, help=HELP_TEXT)

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user:
            return {"message": f"User {data['username']} already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": CREATED}, 201
