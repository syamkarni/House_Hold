from flask import request, jsonify
import os
from flask_restful import Resource, Api
from application.data.model import db, User, Role, UserRole
from . import auth_bp

auth_api = Api(auth_bp)

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        u_mail = data.get('u_mail')
        password = data.get('password')
        role_name = data.get('role')

        if not u_mail or not password or not role_name:
            return {'status': 'failed', 'message': 'Email, password, and role are required'}, 400

        user = User.query.filter_by(u_mail=u_mail).first()
        if user:
            return {'status': 'failed', 'message': 'This email is already registered'}, 409

        new_user = User(u_mail=u_mail, fs_uniquifier=os.urandom(16).hex())
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()  # Ensure new_user.user_id is available

        role = Role.query.filter_by(name=role_name).first()
        if not role:
            db.session.rollback()
            return {'status': 'failed', 'message': 'Role not found'}, 404

        # Assign the role to the user
        user_role = UserRole(user_id=new_user.user_id, role_id=role.id)
        db.session.add(user_role)
        db.session.commit()

        return {'status': 'success', 'message': 'User registered successfully'}, 201

auth_api.add_resource(RegisterAPI, '/register')
