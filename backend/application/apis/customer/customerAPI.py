from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.model import ServiceRequest, Customer, db
from sqlalchemy.exc import SQLAlchemyError
import datetime

customer_bp = Blueprint('customer_bp', __name__)
customer_api = Api(customer_bp)

class CreateServiceRequest(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            service_id = data['service_id']
            date_of_request = data.get('date_of_request', datetime.datetime.utcnow())
            remarks = data.get('remarks')

            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'customer' not in roles:
                return {'message': 'Unauthorized: Only customers can create service requests'}, 403

            customer = Customer.query.filter_by(user_id=user_id).first()
            if not customer:
                return {'message': 'Customer profile not found'}, 404

            new_request = ServiceRequest(
                service_id=service_id,
                customer_id=customer.id,
                date_of_request=date_of_request,
                service_status='requested',
                remarks=remarks
            )
            db.session.add(new_request)
            db.session.commit()
            return {'message': 'Service request created successfully', 'request_id': new_request.id}, 201

        except KeyError as e:
            return {'message': 'Missing required data', 'error': str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while creating service request', 'error': str(e)}, 500

class EditServiceRequest(Resource):
    @jwt_required()
    def put(self, request_id):
        data = request.get_json()
        try:
            service_request = ServiceRequest.query.get_or_404(request_id)

            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'customer' not in roles:
                return {'message': 'Unauthorized: Only customers can edit service requests'}, 403

            customer = Customer.query.filter_by(user_id=user_id).first()
            if not customer or service_request.customer_id != customer.id:
                return {'message': 'Unauthorized access to edit this service request'}, 403

            if service_request.service_status not in ['requested', 'assigned']:
                return {'message': 'Service request cannot be edited at this stage'}, 400

            service_request.date_of_request = data.get('date_of_request', service_request.date_of_request)
            service_request.remarks = data.get('remarks', service_request.remarks)
            db.session.commit()
            return {'message': 'Service request updated successfully!'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while updating service request', 'error': str(e)}, 500

class CloseServiceRequest(Resource):
    @jwt_required()
    def put(self, request_id):
        try:
            service_request = ServiceRequest.query.get_or_404(request_id)

            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'customer' not in roles:
                return {'message': 'Unauthorized: Only customers can close service requests'}, 403

            customer = Customer.query.filter_by(user_id=user_id).first()
            if not customer or service_request.customer_id != customer.id:
                return {'message': 'Unauthorized access to close this service request'}, 403

            if service_request.service_status != 'assigned':
                return {'message': 'Only assigned requests can be closed'}, 400

            service_request.service_status = 'closed'
            service_request.date_of_completion = datetime.datetime.utcnow()
            db.session.commit()
            return {'message': 'Service request closed successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while closing service request', 'error': str(e)}, 500


customer_api.add_resource(CreateServiceRequest, '/customer/service_request')
customer_api.add_resource(EditServiceRequest, '/customer/service_request/<int:request_id>')
customer_api.add_resource(CloseServiceRequest, '/customer/service_request/<int:request_id>/close')