from flask import request
from flask_restful import Resource
from models.user import UserModel
from schemas.user import UserSchema
from marshmallow import ValidationError
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
        create_access_token,
        create_refresh_token,
        jwt_refresh_token_required,
        get_jwt_identity,
        jwt_required,
        get_raw_jwt,
        )
from blacklist import BLACKLIST

HELP_TEXT = "Field required."
CREATED = "User created succesfully."
DELETED = "User deleted succesfully."
USER_NOT_FOUND = "No user found with that id."
INVALID_CREDENTIALS = "Incorrect username or password."
LOGOUT = "Succesfully logged out."
NOT_CONFIRMED_ERROR = "You have not confirmed registration, please check your email <{}>."
ACTIVATED = "User has been activated succesfully."

user_schema = UserSchema()

class UserRegister(Resource):

    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())
        if UserModel.find_by_username(user.username):
            return {"message": f"User {data['username']} already exists."}, 400

        user.save_to_db()
        return {"message": CREATED}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        user.delete_from_db()
        return {"message": DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user_data.password, user.password):
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            else:
                return {"message": NOT_CONFIRMED_ERROR.format(user.username)}, 400

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": LOGOUT}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.activated = True
            user.save_to_db()
            return {'message': ACTIVATED}, 200
        else:
            return {'message': USER_NOT_FOUND}, 404
