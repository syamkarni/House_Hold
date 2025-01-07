from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.model import User, ServiceProfessional, Service, db
from sqlalchemy.exc import SQLAlchemyError

admin_bp = Blueprint('admin_bp', __name__)
admin_api = Api(admin_bp)

class ApproveProfessional(Resource):
    @jwt_required()
    def put(self, professional_id):
        try:
            identity = get_jwt_identity()
            roles = identity['roles']
            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            professional = ServiceProfessional.query.get_or_404(professional_id)
            if professional.approved:
                return {'message': 'Professional is already approved'}, 400

            professional.approved = True
            db.session.commit()
            return {'message': 'Service professional approved successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while approving professional', 'error': str(e)}, 500

class BlockUser(Resource):
    @jwt_required()
    def put(self, user_id):
        try:
            identity = get_jwt_identity()
            roles = identity['roles']
            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            user = User.query.get_or_404(user_id)
            user.active = False

            if user.customer:
                user.customer.is_blocked = True

            if user.service_professional:
                user.service_professional.is_blocked = True

            db.session.commit()
            return {'message': 'User blocked successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while blocking user', 'error': str(e)}, 500

class UnblockUser(Resource):
    @jwt_required()
    def put(self, user_id):
        try:
            identity = get_jwt_identity()
            roles = identity['roles']
            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            user = User.query.get_or_404(user_id)
            user.active = True

            if user.customer:
                user.customer.is_blocked = False

            if user.service_professional:
                user.service_professional.is_blocked = False

            db.session.commit()
            return {'message': 'User unblocked successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while unblocking user', 'error': str(e)}, 500

class CreateService(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            identity = get_jwt_identity()
            roles = identity['roles']
            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            name = data['name']
            price = data['price']
            time_required = data.get('time_required')
            description = data.get('description')

            if Service.query.filter_by(name=name).first():
                return {'message': 'Service already exists'}, 400

            new_service = Service(
                name=name,
                price=price,
                time_required=time_required,
                description=description
            )
            db.session.add(new_service)
            db.session.commit()
            return {'message': 'Service created successfully', 'service_id': new_service.id}, 201
        except KeyError as e:
            return {'message': f'Missing required field: {e}'}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while creating service', 'error': str(e)}, 500
        
class GetUsers(Resource):
    @jwt_required()
    def get(self):
        try:
            identity = get_jwt_identity()
            roles = identity['roles']
            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            users = User.query.all()
            users_data = [
                {
                    "user_id": user.user_id,
                    "u_mail": user.u_mail,
                    "roles": [role.name for role in user.roles],
                    "is_blocked": not user.active
                }
                for user in users
            ]

            return {"users": users_data}, 200
        except SQLAlchemyError as e:
            return {'message': 'An error occurred while fetching users', 'error': str(e)}, 500


class UpdateService(Resource):
    @jwt_required()
    def put(self, service_id):
        data = request.get_json()
        try:
            identity = get_jwt_identity()
            roles = identity['roles']
            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            service = Service.query.get_or_404(service_id)
            service.name = data.get('name', service.name)
            service.price = data.get('price', service.price)
            service.time_required = data.get('time_required', service.time_required)
            service.description = data.get('description', service.description)

            db.session.commit()
            return {'message': 'Service updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while updating service', 'error': str(e)}, 500

class DeleteService(Resource):
    @jwt_required()
    def delete(self, service_id):
        try:
            identity = get_jwt_identity()
            roles = identity['roles']
            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            service = Service.query.get_or_404(service_id)
            db.session.delete(service)
            db.session.commit()
            return {'message': 'Service deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while deleting service', 'error': str(e)}, 500
        
class PendingProfessionals(Resource):
    @jwt_required()
    def get(self):
        try:
            identity = get_jwt_identity()
            roles = identity['roles']

            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            pending_professionals = ServiceProfessional.query.filter_by(approved=False).all()


            professionals_data = [
                {
                    "id": professional.id,
                    "name": professional.name,
                    "service_type": professional.service.name if professional.service else None,
                    "experience": professional.experience,
                    "description": professional.description
                }
                for professional in pending_professionals
            ]

            return {"professionals": professionals_data}, 200
        except SQLAlchemyError as e:
            return {'message': 'An error occurred while fetching pending professionals', 'error': str(e)}, 500


class RejectProfessional(Resource):
    @jwt_required()
    def delete(self, professional_id):
        try:
            identity = get_jwt_identity()
            roles = identity['roles']

            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            professional = ServiceProfessional.query.get_or_404(professional_id)

            if professional.approved:
                return {'message': 'Cannot reject an already approved professional'}, 400
            db.session.delete(professional)
            db.session.commit()

            return {'message': 'Service professional rejected successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while rejecting professional', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500






admin_api.add_resource(ApproveProfessional, '/admin/professional/<int:professional_id>/approve')
admin_api.add_resource(BlockUser, '/admin/user/<int:user_id>/block')
admin_api.add_resource(UnblockUser, '/admin/user/<int:user_id>/unblock')
admin_api.add_resource(CreateService, '/admin/service')
admin_api.add_resource(UpdateService, '/admin/service/<int:service_id>')
admin_api.add_resource(DeleteService, '/admin/service/<int:service_id>')
admin_api.add_resource(GetUsers, '/admin/users')
admin_api.add_resource(PendingProfessionals, '/admin/professionals/pending')
admin_api.add_resource(RejectProfessional, '/admin/professional/<int:professional_id>/reject')
