from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.model import Service, ServiceRequest, Customer, Review, db, Package
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
import datetime
from application.cache import cache
from application.tasks import notify_customer_action

customer_bp = Blueprint('customer_bp', __name__)
customer_api = Api(customer_bp)

class ListAvailableServices(Resource):
    @jwt_required()
    def get(self):
        try:
            services = Service.query.all()
            service_list = []
            for service in services:
                packages = [{
                    'id': pkg.id,
                    'name': pkg.name,
                    'description': pkg.description,
                    'price': pkg.price,
                    'time_required': pkg.time_required
                } for pkg in service.packages]

                service_list.append({
                    'id': service.id,
                    'name': service.name,
                    'description': service.description,
                    'base_price': service.price,
                    'time_required': service.time_required,
                    'packages': packages
                })

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
                        'phone': r.professional.phone,
                        # 'service_type': r.professional.service_type,
                        'service_name': r.professional.service.name if r.professional.service else None,
                        'experience': r.professional.experience,
                        'description': r.professional.description
                    }

                review_exists = Review.query.filter_by(service_request_id=r.id).first() is not None

                package_data = None
                if r.package:
                    package_data = {
                        'id': r.package.id,
                        'name': r.package.name,
                        'description': r.package.description,
                        'price': r.package.price,
                        'time_required': r.package.time_required
                    }

                request_dict = {
                    'id': r.id,
                    'service_id': r.service_id,
                    'service': service_data,
                    'professional_id': r.professional_id,
                    'professional': professional_data,
                    'package': package_data,
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
            package_id = data.get('package_id')  
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
                package_id=package_id,
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
            user_email = customer.user.u_mail
            notify_customer_action.delay(user_email, "cancel_service_request", extra_info=f"Request ID={request_id}")
            return {'message': 'Service request cancelled successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while cancelling service request', 'error': str(e)}, 500
        
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
                return {'message': 'Unauthorized access to this service request'}, 403

            if service_request.service_status != 'assigned':
                return {'message': 'Service request cannot be closed at this stage'}, 400

            service_request.service_status = 'completed'
            service_request.date_of_completion = datetime.datetime.utcnow()
            db.session.commit()

            user_email = customer.user.u_mail
            notify_customer_action.delay(user_email, "close_service_request", extra_info=f"Request ID={request_id}")


            return {'message': 'Service request closed successfully'}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'message': 'An error occurred while closing service request',
                'error': str(e)
            }, 500

class ProvideReview(Resource):
    @jwt_required()
    def post(self, request_id):
        try:
            data = request.get_json()
            rating = data.get('rating')
            comment = data.get('comment')

            if not rating or not (1 <= rating <= 6):
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

            user_email = customer.user.u_mail
            notify_customer_action.delay(user_email, "provide_review", extra_info=f"Rating={rating}, Comment={comment}")

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

class CustomerSearchAPI(Resource):
    @jwt_required()
    def get(self):
        """
        Search either services or packages by name.
        Request params:
          category = "services" or "packages"
          searchTerm = string
        """
        try:
            identity = get_jwt_identity()
            roles = identity.get('roles', [])
            if 'customer' not in roles:
                return {'message': 'Unauthorized: Only customers can search'}, 403

            category = request.args.get('category', '').lower()
            search_term = request.args.get('searchTerm', '')

            if category == 'services':
                services = Service.query.filter(Service.name.ilike(f"%{search_term}%")).all()
                service_list = []
                for svc in services:
                    packages_data = []
                    for pkg in svc.packages:
                        packages_data.append({
                            'id': pkg.id,
                            'name': pkg.name,
                            'price': pkg.price,
                            'description': pkg.description,
                            'time_required': pkg.time_required
                        })

                    service_list.append({
                        'id': svc.id,
                        'name': svc.name,
                        'description': svc.description,
                        'base_price': svc.price,
                        'time_required': svc.time_required,
                        'packages': packages_data
                    })
                return {'services': service_list}, 200

            elif category == 'packages':
                packages = Package.query.filter(Package.name.ilike(f"%{search_term}%")).all()
                package_list = []
                for pkg in packages:
                    service_data = None
                    if pkg.service:
                        service_data = {
                            'id': pkg.service.id,
                            'name': pkg.service.name
                        }
                    package_list.append({
                        'id': pkg.id,
                        'name': pkg.name,
                        'description': pkg.description,
                        'price': pkg.price,
                        'time_required': pkg.time_required,
                        'service': service_data
                    })
                return {'packages': package_list}, 200

            else:
                return {'message': "Invalid category. Must be 'services' or 'packages'."}, 400

        except SQLAlchemyError as e:
            return {'message': 'Database error occurred while searching', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'Unexpected error', 'error': str(e)}, 500
        
class CustomerSummaryAPI(Resource):
    @jwt_required()
    @cache.memoize(timeout=60)
    def get(self):
        """
        Returns summary data for the authenticated customer.
        """
        try:
            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']
            if 'customer' not in roles:
                return {'message': 'Unauthorized: Only customers can access summary'}, 403

            customer = Customer.query.filter_by(user_id=user_id).first()
            if not customer:
                return {'message': 'Customer profile not found'}, 404

            total_requests = ServiceRequest.query.filter_by(customer_id=customer.id).count()

            completed_requests = ServiceRequest.query.filter_by(
                customer_id=customer.id,
                service_status='completed'
            ).count()

            canceled_requests = ServiceRequest.query.filter_by(
                customer_id=customer.id,
                service_status='cancelled'
            ).count()

            average_rating_given = db.session.query(func.avg(Review.rating)).filter_by(
                customer_id=customer.id
            ).scalar()
            average_rating_given = round(average_rating_given, 2) if average_rating_given else 0

            rating_rows = (
                db.session.query(Review.rating, func.count(Review.rating))
                .filter_by(customer_id=customer.id)
                .group_by(Review.rating)
                .all()
            )
            distribution_dict = {row[0]: row[1] for row in rating_rows}

            rating_distribution = []
            for r in range(1, 6):
                rating_distribution.append({
                    "rating": r,
                    "count": distribution_dict.get(r, 0)
                })

            summary = {
                "total_requests": total_requests,
                "completed_requests": completed_requests,
                "canceled_requests": canceled_requests,
                "average_rating_given": average_rating_given,
                "rating_distribution": rating_distribution
            }

            return {"summary": summary}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": "An error occurred while fetching customer summary",
                "error": str(e)
            }, 500
        except Exception as e:
            return {
                "message": "Unexpected error occurred",
                "error": str(e)
            }, 500





customer_api.add_resource(ListAvailableServices, '/customer/services')
customer_api.add_resource(CustomerServiceRequests, '/customer/service_requests')
customer_api.add_resource(CreateServiceRequest, '/customer/service_request')
customer_api.add_resource(EditServiceRequest, '/customer/service_request/<int:request_id>')
customer_api.add_resource(CancelServiceRequest, '/customer/service_request/<int:request_id>/cancel')
customer_api.add_resource(ProvideReview, '/customer/service_request/<int:request_id>/review')
customer_api.add_resource(CustomerProfileAPI, '/customer/profile')
customer_api.add_resource(CloseServiceRequest, '/customer/service_request/<int:request_id>/close')
customer_api.add_resource(CustomerSearchAPI, '/customer/search')
customer_api.add_resource(CustomerSummaryAPI, '/customer/summary')
