from flask import Blueprint, jsonify
from flask_restful import Resource, reqparse, Api
from flask_security import login_user
from flask_security.utils import verify_password
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)

from application.data.model import db, User, UserRole

# Initialize Blueprint
auth_bp = Blueprint('auth_bp', __name__)
auth_api = Api(auth_bp)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("u_mail", type=str, required=True, help="User mail is required!")
user_post_args.add_argument("password", type=str, required=True, help="Password is required!")

class LoginAPI(Resource):
    def post(self):
        args = user_post_args.parse_args()
        u_mail = args.get('u_mail')
        password = args.get('password')

        user = User.query.filter_by(u_mail=u_mail).first()

        if user is None:
            return {'status': 'failed', 'message': 'User not found (This email is not registered)'}, 404
        if not verify_password(password, user.password):
            return {'status': 'failed', 'message': 'Wrong password'}, 401

        user_role = UserRole.query.filter_by(user_id=user.user_id).first()
        role_name = user_role.role.name if user_role else 'No role assigned'

        refresh_token = create_refresh_token(identity=user.user_id)
        access_token = create_access_token(identity=user.user_id)

        login_user(user)

        return {
            'status': 'success',
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'u_mail': user.u_mail,
            'role': role_name
        }, 200

class RefreshTokenAPI(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {'access_token': access_token}, 200

# Add resources to the Api
auth_api.add_resource(LoginAPI, '/login')
auth_api.add_resource(RefreshTokenAPI, '/refresh')
