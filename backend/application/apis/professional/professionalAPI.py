from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.model import ServiceRequest, ServiceProfessional, db
from sqlalchemy.exc import SQLAlchemyError
import datetime

professional_bp = Blueprint('professional_bp', __name__)
professional_api = Api(professional_bp)

class ListAssignedServiceRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'professional' not in roles:
                return {'message': 'Unauthorized: Only professionals can access this endpoint'}, 403

            professional = ServiceProfessional.query.filter_by(user_id=user_id).first()
            if not professional:
                return {'message': 'Professional profile not found'}, 404

            requests = ServiceRequest.query.filter_by(professional_id=professional.id).all()
            request_list = []
            for r in requests:
                service_data = None
                if r.service:
                    service_data = {
                        'id': r.service.id,
                        'name': r.service.name,
                        'description': r.service.description,
                        'price': r.service.price,
                        'time_required': r.service.time_required
                    }

                request_dict = {
                    'id': r.id,
                    'service_id': r.service_id,
                    'service': service_data,
                    'customer_id': r.customer_id,
                    'date_of_request': r.date_of_request.isoformat(),
                    'service_status': r.service_status,
                    'remarks': r.remarks
                }
                request_list.append(request_dict)

            return {'requests': request_list}, 200
        except SQLAlchemyError as e:
            return {
                'message': 'An error occurred while fetching service requests',
                'error': str(e)
            }, 500

class AcceptServiceRequest(Resource):
    @jwt_required()
    def put(self, request_id):
        try:
            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'professional' not in roles:
                return {'message': 'Unauthorized: Only professionals can accept service requests'}, 403

            professional = ServiceProfessional.query.filter_by(user_id=user_id).first()
            if not professional:
                return {'message': 'Professional profile not found'}, 404

            service_request = ServiceRequest.query.get_or_404(request_id)
            if service_request.service_status != 'requested':
                return {'message': 'Service request is not in a state that can be accepted'}, 400

            service_request.professional_id = professional.id
            service_request.service_status = 'assigned'
            db.session.commit()
            return {'message': 'Service request accepted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while accepting service request', 'error': str(e)}, 500

class RejectServiceRequest(Resource):
    @jwt_required()
    def put(self, request_id):
        try:
            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'professional' not in roles:
                return {'message': 'Unauthorized: Only professionals can reject service requests'}, 403

            professional = ServiceProfessional.query.filter_by(user_id=user_id).first()
            if not professional:
                return {'message': 'Professional profile not found'}, 404

            service_request = ServiceRequest.query.get_or_404(request_id)
            if service_request.service_status != 'requested':
                return {'message': 'Service request cannot be rejected at this stage'}, 400

            service_request.service_status = 'rejected'
            db.session.commit()
            return {'message': 'Service request rejected successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while rejecting service request', 'error': str(e)}, 500

class CompleteServiceRequest(Resource):
    @jwt_required()
    def put(self, request_id):
        try:
            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'professional' not in roles:
                return {'message': 'Unauthorized: Only professionals can complete service requests'}, 403

            professional = ServiceProfessional.query.filter_by(user_id=user_id).first()
            if not professional:
                return {'message': 'Professional profile not found'}, 404

            service_request = ServiceRequest.query.get_or_404(request_id)
            if service_request.professional_id != professional.id:
                return {'message': 'Unauthorized access to complete this service request'}, 403

            if service_request.service_status != 'assigned':
                return {'message': 'Only assigned requests can be marked as completed'}, 400

            service_request.service_status = 'completed'
            service_request.date_of_completion = datetime.datetime.utcnow()
            db.session.commit()
            return {'message': 'Service request completed successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while completing service request', 'error': str(e)}, 500


professional_api.add_resource(ListAssignedServiceRequests, '/professional/service_requests')
professional_api.add_resource(AcceptServiceRequest, '/professional/service_request/<int:request_id>/accept')
professional_api.add_resource(RejectServiceRequest, '/professional/service_request/<int:request_id>/reject')
professional_api.add_resource(CompleteServiceRequest, '/professional/service_request/<int:request_id>/complete')
