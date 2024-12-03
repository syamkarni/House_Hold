from flask import request, jsonify
import os
from flask_restful import Resource, Api
from application.data.model import db, User, Role, UserRole, Customer, ServiceProfessional
from . import auth_bp
import datetime

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
        db.session.flush()  


        role = Role.query.filter_by(name=role_name).first()
        if not role:
            db.session.rollback()
            return {'status': 'failed', 'message': 'Role not found'}, 404

        user_role = UserRole(user_id=new_user.user_id, role_id=role.id)
        db.session.add(user_role)

        if role_name == 'customer':

            new_customer = Customer(
                user_id=new_user.user_id,
                name=data.get('name', ''),  # You may prompt for name, phone, address in registration
                phone=data.get('phone', ''),
                address=data.get('address', ''),
                is_blocked=False
            )
            db.session.add(new_customer)
        elif role_name == 'professional':
            # Create a Service Professional profile
            new_professional = ServiceProfessional(
                user_id=new_user.user_id,
                name=data.get('name', ''),
                description=data.get('description', ''),
                service_type=data.get('service_type', ''),
                experience=data.get('experience', 0),
                approved=False,  # You may have an admin approve professionals
                date_created=datetime.datetime.utcnow(),
                is_blocked=False
            )
            db.session.add(new_professional)

        # Commit all changes
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'status': 'failed', 'message': 'An error occurred during registration', 'error': str(e)}, 500

        return {'status': 'success', 'message': 'User registered successfully'}, 201

auth_api.add_resource(RegisterAPI, '/register')
