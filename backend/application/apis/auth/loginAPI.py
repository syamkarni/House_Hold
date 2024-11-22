from flask import request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from application.data.model import db, User, UserRole, Role
from . import auth_bp

auth_api = Api(auth_bp)

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        u_mail = data.get('u_mail')
        password = data.get('password')

        if not u_mail or not password:
            return {'status': 'failed', 'message': 'Email and password are required'}, 400

        user = User.query.filter_by(u_mail=u_mail).first()
        if user is None:
            return {'status': 'failed', 'message': 'User not found (This email is not registered)'}, 404

        if not user.check_password(password):
            return {'status': 'failed', 'message': 'Wrong password'}, 401

        roles = user.get_roles()

        access_token = create_access_token(identity={'user_id': user.user_id, 'roles': roles})
        refresh_token = create_refresh_token(identity={'user_id': user.user_id, 'roles': roles})

        return {
            'status': 'success',
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'u_mail': user.u_mail,
            'roles': roles
        }, 200

class RefreshTokenAPI(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {'access_token': access_token}, 200

auth_api.add_resource(LoginAPI, '/login')
auth_api.add_resource(RefreshTokenAPI, '/refresh')
