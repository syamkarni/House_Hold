from flask import request, jsonify
import os
from flask_restful import Resource, Api
from application.data.model import db, User, Role, UserRole, Customer, ServiceProfessional, Service
from . import auth_bp
import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s : %(message)s',
    handlers=[
        logging.FileHandler("register_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

auth_api = Api(auth_bp)

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        u_mail = data.get('u_mail')
        password = data.get('password')
        role_name = data.get('role')

        if not u_mail or not password or not role_name:
            logger.warning("Registration failed: Missing email, password, or role.")
            return {'status': 'failed', 'message': 'Email, password, and role are required'}, 400

        user = User.query.filter_by(u_mail=u_mail).first()
        if user:
            logger.warning(f"Registration failed: Email {u_mail} is already registered.")
            return {'status': 'failed', 'message': 'This email is already registered'}, 409


        new_user = User(u_mail=u_mail, fs_uniquifier=os.urandom(16).hex())
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()  


        role = Role.query.filter_by(name=role_name).first()
        if not role:
            db.session.rollback()
            logger.error(f"Registration failed: Role '{role_name}' not found.")
            return {'status': 'failed', 'message': 'Role not found'}, 404

        user_role = UserRole(user_id=new_user.user_id, role_id=role.id)
        db.session.add(user_role)

        if role_name == 'customer':
            new_customer = Customer(
                user_id=new_user.user_id,
                name=data.get('name', ''),  
                phone=data.get('phone', ''),
                address=data.get('address', ''),
                is_blocked=False
            )
            db.session.add(new_customer)
            logger.info(f"Registered new customer: {u_mail}")
        elif role_name == 'professional':
            service_id = data.get('service_id')  
            service = None
            if service_id:
                service = Service.query.get(service_id)
                if not service:
                    db.session.rollback()
                    logger.warning(f"Registration failed: Service with id {service_id} does not exist.")
                    return {'status': 'failed', 'message': 'Invalid service_id provided'}, 400

            new_professional = ServiceProfessional(
                user_id=new_user.user_id,
                name=data.get('name', '').strip(),
                description=data.get('description', ''),
                service_id=service_id,  
                experience=data.get('experience', 0),
                approved=False,  # Pending admin approval
                date_created=datetime.datetime.utcnow(),
                is_blocked=False
            )
            db.session.add(new_professional)
            logger.info(f"Registered new professional: {u_mail} with service_id {service_id}")
        else:
            db.session.rollback()
            logger.warning(f"Registration failed: Unsupported role '{role_name}'.")
            return {'status': 'failed', 'message': 'Unsupported role'}, 400


        try:
            db.session.commit()
            logger.info(f"User registered successfully: {u_mail} as {role_name}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration failed for {u_mail}: {e}")
            return {'status': 'failed', 'message': 'An error occurred during registration', 'error': str(e)}, 500

        return {'status': 'success', 'message': 'User registered successfully'}, 201

auth_api.add_resource(RegisterAPI, '/register')
