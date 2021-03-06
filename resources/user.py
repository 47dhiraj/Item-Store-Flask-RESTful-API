from flask_restful import Resource, reqparse
from hmac import compare_digest

from flask_jwt_extended import (create_access_token,
create_refresh_token,jwt_required,get_jwt_identity)

from models.user import UserModel                          


_user_parser = reqparse.RequestParser()                       

_user_parser.add_argument('username',                        
                    type = str,
                    required = True,
                    help = "Username field cannot be left blank!"
                    )

_user_parser.add_argument('password',                       
                    type = str,
                    required = True,
                    help = "Password field cannot be left blank!"
                    )


class UserRegister(Resource):                               

    def post(self):                                         
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):    
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)                           
        # Alternative Code ==> # user = UserModel(data['username'], data['password'])

        user.save_to_db()                                   

        return {"message": "User created successfully."}, 201   




class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        # authentication user by checking password
        if user and compare_digest(user.password, data['password']):

            access_token = create_access_token(identity = user.id, fresh=True)              
            refresh_token = create_refresh_token(user.id)                                   

            return {                                                                        
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }, 200

        return {"message": "Invalid Credentials!"}, 401                                     


class TokenRefresh(Resource):
    @jwt_required(refresh=True)                         
    def post(self):
        current_user = get_jwt_identity()                                                   

        new_token = create_access_token(identity = current_user, fresh = False)             

        return {'access_token': new_token}, 200                                             




# class User(Resource):
#     """
#     This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
#     sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
#     """
#     @classmethod
#     def get(cls, user_id: int):
#         user = UserModel.find_by_id(user_id)

#         if not user:
#             return {'message': 'User Not Found'}, 404

#         return user.json(), 200

#     @classmethod
#     def delete(cls, user_id: int):
#         user = UserModel.find_by_id(user_id)

#         if not user:
#             return {'message': 'User Not Found'}, 404

#         user.delete_from_db()

#         return {'message': 'User deleted.'}, 200

