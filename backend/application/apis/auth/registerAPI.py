from flask import Blueprint, jsonify
import secrets
#from werkzeug.security import generate_password_hash
from flask_security.utils import hash_password
from flask_restful import Resource, reqparse, Api
from application.data.model import db, User, Role, UserRole

from . import auth_bp

auth_api = Api(auth_bp)


user_post_args = reqparse.RequestParser()
user_post_args.add_argument('u_mail', type=str, required=True, help='User mail is required to register!')
user_post_args.add_argument('password', type=str, required=True, help='Password is required to register!')
user_post_args.add_argument('role', type=str, required=True, help='Role is required to register!')

class RegisterAPI(Resource):
    def post(self):
        args = user_post_args.parse_args()
        u_mail = args.get('u_mail')
        password = args.get('password')
        role_name = args.get('role')

        print(f"Attempting to register user with email: {u_mail}, role: {role_name}")

        user = User.query.filter_by(u_mail=u_mail).first()
        if user:
            return {'status': 'failed', 'message': 'This email is already registered'}, 409

        hashed_password = hash_password(password)
        fs_uniquifier = secrets.token_hex(16)

        new_user = User(u_mail=u_mail, password=hashed_password, fs_uniquifier=fs_uniquifier)
        db.session.add(new_user)
        db.session.flush()  

        role = Role.query.filter_by(name=role_name).first()
        if not role:
            db.session.rollback()
            return {'status': 'failed', 'message': 'Role not found'}, 404

        new_user_role = UserRole(user_id=new_user.user_id, role_id=role.id)
        db.session.add(new_user_role)
        db.session.commit()

        print(f"User {u_mail} registered successfully with role {role_name}")
        return {'status': 'success', 'message': 'User registered successfully'}, 201

auth_api.add_resource(RegisterAPI, '/register')
