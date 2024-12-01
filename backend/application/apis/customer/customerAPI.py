from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.model import Service, ServiceRequest, Customer, Review, db
from sqlalchemy.exc import SQLAlchemyError
import datetime

customer_bp = Blueprint('customer_bp', __name__)
customer_api = Api(customer_bp)

class ListAvailableServices(Resource):
    @jwt_required()
    def get(self):
        try:
            services = Service.query.all()
            service_list = [{
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': service.price,
                'time_required': service.time_required
            } for service in services]
            return {'services': service_list}, 200
        except SQLAlchemyError as e:
            return {
                'message': 'An error occurred while fetching services',
                'error': str(e)
            }, 500

class CustomerServiceRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'customer' not in roles:
                return {'message': 'Unauthorized: Only customers can access this endpoint'}, 403

            customer = Customer.query.filter_by(user_id=user_id).first()
            if not customer:
                return {'message': 'Customer profile not found'}, 404

            requests = ServiceRequest.query.filter_by(customer_id=customer.id).all()
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

                professional_data = None
                if r.professional:
                    professional_data = {
                        'id': r.professional.id,
                        'name': r.professional.name,
                        'service_type': r.professional.service_type,
                        'experience': r.professional.experience,
                        'description': r.professional.description
                    }

                review_exists = Review.query.filter_by(service_request_id=r.id).first() is not None

                request_dict = {
                    'id': r.id,
                    'service_id': r.service_id,
                    'service': service_data,
                    'professional_id': r.professional_id,
                    'professional': professional_data,
                    'date_of_request': r.date_of_request.isoformat(),
                    'date_of_completion': r.date_of_completion.isoformat() if r.date_of_completion else None,
                    'service_status': r.service_status,
                    'remarks': r.remarks,
                    'reviewed': review_exists
                }
                request_list.append(request_dict)

            return {'requests': request_list}, 200
        except SQLAlchemyError as e:
            return {
                'message': 'An error occurred while fetching service requests',
                'error': str(e)
            }, 500

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

            service = Service.query.get(service_id)
            if not service:
                return {'message': 'Service not found'}, 404

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
            return {'message': 'Service request updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while updating service request', 'error': str(e)}, 500

class CancelServiceRequest(Resource):
    @jwt_required()
    def put(self, request_id):
        try:
            service_request = ServiceRequest.query.get_or_404(request_id)

            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'customer' not in roles:
                return {'message': 'Unauthorized: Only customers can cancel service requests'}, 403

            customer = Customer.query.filter_by(user_id=user_id).first()
            if not customer or service_request.customer_id != customer.id:
                return {'message': 'Unauthorized access to cancel this service request'}, 403

            if service_request.service_status not in ['requested', 'assigned']:
                return {'message': 'Service request cannot be cancelled at this stage'}, 400

            service_request.service_status = 'cancelled'
            db.session.commit()
            return {'message': 'Service request cancelled successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while cancelling service request', 'error': str(e)}, 500

class ProvideReview(Resource):
    @jwt_required()
    def post(self, request_id):
        try:
            data = request.get_json()
            rating = data.get('rating')
            comment = data.get('comment')

            if not rating or not (1 <= rating <= 5):
                return {'message': 'Rating must be an integer between 1 and 5'}, 400

            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']

            if 'customer' not in roles:
                return {'message': 'Unauthorized: Only customers can provide reviews'}, 403

            customer = Customer.query.filter_by(user_id=user_id).first()
            if not customer:
                return {'message': 'Customer profile not found'}, 404

            service_request = ServiceRequest.query.get_or_404(request_id)
            if service_request.customer_id != customer.id:
                return {'message': 'Unauthorized access to this service request'}, 403

            if service_request.service_status != 'completed':
                return {'message': 'Cannot review a service request that is not completed'}, 400

            existing_review = Review.query.filter_by(service_request_id=service_request.id).first()
            if existing_review:
                return {'message': 'Review already exists for this service request'}, 400

            new_review = Review(
                service_request_id=service_request.id,
                customer_id=customer.id,
                professional_id=service_request.professional_id,
                rating=rating,
                comment=comment,
                date_posted=datetime.datetime.utcnow()
            )
            db.session.add(new_review)
            db.session.commit()

            return {'message': 'Review submitted successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'message': 'An error occurred while submitting the review',
                'error': str(e)
            }, 500

class CustomerProfileAPI(Resource):
    @jwt_required()
    def get(self):
        """Retrieve the customer's current profile."""
        identity = get_jwt_identity()
        user_id = identity['user_id']
        customer = Customer.query.filter_by(user_id=user_id).first()

        if not customer:
            return {'message': 'Customer profile not found'}, 404

        profile = {
            'name': customer.name,
            'phone': customer.phone,
            'address': customer.address
        }
        return {'profile': profile}, 200

    @jwt_required()
    def put(self):
        """Update the customer's profile."""
        identity = get_jwt_identity()
        user_id = identity['user_id']
        data = request.get_json()
        customer = Customer.query.filter_by(user_id=user_id).first()

        if not customer:
            return {'message': 'Customer profile not found'}, 404


        name = data.get('name')
        phone = data.get('phone')
        address = data.get('address')

        if not all([name, phone, address]):
            return {'message': 'Name, phone, and address are required'}, 400


        customer.name = name
        customer.phone = phone
        customer.address = address

        try:
            db.session.commit()
            return {'message': 'Profile updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while updating profile', 'error': str(e)}, 500


customer_api.add_resource(ListAvailableServices, '/customer/services')
customer_api.add_resource(CustomerServiceRequests, '/customer/service_requests')
customer_api.add_resource(CreateServiceRequest, '/customer/service_request')
customer_api.add_resource(EditServiceRequest, '/customer/service_request/<int:request_id>')
customer_api.add_resource(CancelServiceRequest, '/customer/service_request/<int:request_id>/cancel')
customer_api.add_resource(ProvideReview, '/customer/service_request/<int:request_id>/review')
customer_api.add_resource(CustomerProfileAPI, '/customer/profile')
