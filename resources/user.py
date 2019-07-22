import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from models.user import UserModel



_userparser = reqparse.RequestParser()
_userparser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."

    )
_userparser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )



class UserRegister(Resource):
    def post(self):
        data = _userparser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": " User with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User '{}' created succesfully.".format(data['username'])}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()


    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This username cannot be left null"
                    )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="The password must not be null or invalid"

                     )
    @classmethod
    def post(cls):
        #get data from JSON parser
        data = _userparser.parse_args()
        #finds user in DB
        user = UserModel.find_by_username(data['username'])
        #validates password argument
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False) 
        return {'access_token': new_token}, 200


