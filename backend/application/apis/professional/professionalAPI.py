from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.model import ServiceRequest, ServiceProfessional, db, Service, Review
from sqlalchemy.exc import SQLAlchemyError
import datetime
from application.cache import cache

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


            requests = ServiceRequest.query.filter_by(
                professional_id=professional.id,
                service_status='assigned'
            ).all()

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

class ListUnassignedServiceRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            identity = get_jwt_identity()
            roles = identity['roles']

            if 'professional' not in roles:
                return {'message': 'Unauthorized: Only professionals can access this endpoint'}, 403

            requests = ServiceRequest.query.filter_by(service_status='requested', professional_id=None).all()
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
                'message': 'An error occurred while fetching unassigned service requests',
                'error': str(e)
            }, 500

class ListServiceRequestHistory(Resource):
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

            requests = ServiceRequest.query.filter(
                ServiceRequest.professional_id == professional.id,
                ServiceRequest.service_status.in_(['completed', 'rejected'])
            ).all()

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

                review = Review.query.filter_by(service_request_id=r.id).first()
                if review:
                    review_comment = review.comment if review.comment else '-'
                    review_rating = review.rating
                else:
                    review_comment = "Customer Yet to Rate"
                    review_rating = "Not Rated"

                request_dict = {
                    'id': r.id,
                    'service_id': r.service_id,
                    'service': service_data,
                    'customer_id': r.customer_id,
                    'date_of_request': r.date_of_request.isoformat(),
                    'date_of_completion': r.date_of_completion.isoformat() if r.date_of_completion else None,
                    'service_status': r.service_status,
                    'remarks': review_comment,
                    'rating': review_rating
                }
                request_list.append(request_dict)

            return {'requests': request_list}, 200
        except SQLAlchemyError as e:
            return {
                'message': 'An error occurred while fetching service request history',
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

            service_request.professional_id = professional.id
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

class ProfessionalProfileAPI(Resource):
    @jwt_required()
    def get(self):
        """Retrieve the professional's current profile."""
        identity = get_jwt_identity()
        user_id = identity['user_id']
        professional = ServiceProfessional.query.filter_by(user_id=user_id).first()

        if not professional:
            return {'message': 'Professional profile not found'}, 404
        service = Service.query.get(professional.service_id)

        profile = {
            'name': professional.name,
            'service_id': professional.service_id,
            'service_name': service.name if service else None,
            'experience': professional.experience,
            'description': professional.description,
            'approved': professional.approved
        }
        return {'profile': profile}, 200

    @jwt_required()
    def put(self):
        """Update the professional's profile."""
        identity = get_jwt_identity()
        user_id = identity['user_id']
        data = request.get_json()
        professional = ServiceProfessional.query.filter_by(user_id=user_id).first()

        if not professional:
            return {'message': 'Professional profile not found'}, 404

        name = data.get('name')
        service_id = data.get('service_id')  # Updated to handle service_id
        experience = data.get('experience')
        description = data.get('description')

        if not all([name, service_id, experience, description]):
            return {'message': 'Name, service ID, experience, and description are required'}, 400

        professional.name = name
        professional.service_id = service_id  # Updated to use service_id
        professional.experience = experience
        professional.description = description
        professional.approved = False
        

        try:
            db.session.commit()
            return {'message': 'Profile updated successfully. Awaiting admin approval.'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred while updating profile', 'error': str(e)}, 500
        
class GetAvailableServices(Resource):
    @jwt_required()
    def get(self):
        try:
            services = Service.query.all()
            print("Services fetched:", services)  
            service_list = [{'id': service.id, 'name': service.name} for service in services]
            return {'services': service_list}, 200
        except SQLAlchemyError as e:
            print("Error fetching services:", e)  
            return {'message': 'An error occurred while fetching services', 'error': str(e)}, 500

class ProfessionalSearchAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity.get('roles', [])

            if 'professional' not in roles:
                return {'message': 'Unauthorized: Only professionals can access this endpoint'}, 403

            category = request.args.get('category', '')
            search_term = request.args.get('searchTerm', '')
            from_date = request.args.get('fromDate')
            to_date = request.args.get('toDate')

            query = ServiceRequest.query

            if category == 'service':
                query = query.join(Service).filter(Service.name.ilike(f"%{search_term}%"))
            elif category == 'customer_remarks':
                query = query.filter(ServiceRequest.remarks.ilike(f"%{search_term}%"))
            elif category == 'date_of_request':
                if from_date and to_date:
                    query = query.filter(
                        ServiceRequest.date_of_request >= from_date,
                        ServiceRequest.date_of_request <= to_date
                    )
                elif from_date:
                    query = query.filter(ServiceRequest.date_of_request >= from_date)
                elif to_date:
                    query = query.filter(ServiceRequest.date_of_request <= to_date)

            requests = query.all()

            result_list = []
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
                    'service': service_data,
                    'date_of_request': r.date_of_request.isoformat(),
                    'remarks': r.remarks,
                    'service_status': r.service_status
                }
                result_list.append(request_dict)

            return {'requests': result_list}, 200
        except SQLAlchemyError as e:
            return {
                'message': 'An error occurred while searching service requests',
                'error': str(e)
            }, 500

class ProfessionalSummaryAPI(Resource):
    @jwt_required()
    @cache.memoize(timeout=60)
    def get(self):
        try:
            identity = get_jwt_identity()
            user_id = identity['user_id']
            roles = identity['roles']
            if 'professional' not in roles:
                return {'message': 'Unauthorized: Only professionals can access summary'}, 403

            professional = ServiceProfessional.query.filter_by(user_id=user_id).first()
            if not professional:
                return {'message': 'Professional profile not found'}, 404

            assigned_count = ServiceRequest.query.filter_by(
                professional_id=professional.id,
                service_status='assigned'
            ).count()

            completed_count = ServiceRequest.query.filter_by(
                professional_id=professional.id,
                service_status='completed'
            ).count()

            average_rating = db.session.query(db.func.avg(Review.rating)).filter_by(
                professional_id=professional.id
            ).scalar()
            average_rating = round(average_rating, 2) if average_rating else 0

            summary_data = {
                "assigned_count": assigned_count,
                "completed_count": completed_count,
                "average_rating": average_rating
            }

            return {"summary": summary_data}, 200
        except SQLAlchemyError as e:
            return {"message": "An error occurred while fetching professional summary", "error": str(e)}, 500
        except Exception as e:
            return {"message": "Unexpected error occurred", "error": str(e)}, 500






professional_api.add_resource(ListAssignedServiceRequests, '/professional/service_requests')
professional_api.add_resource(ListUnassignedServiceRequests, '/professional/unassigned_service_requests')
professional_api.add_resource(ListServiceRequestHistory, '/professional/service_request_history')
professional_api.add_resource(AcceptServiceRequest, '/professional/service_request/<int:request_id>/accept')
professional_api.add_resource(RejectServiceRequest, '/professional/service_request/<int:request_id>/reject')
professional_api.add_resource(CompleteServiceRequest, '/professional/service_request/<int:request_id>/complete')
professional_api.add_resource(ProfessionalProfileAPI, '/professional/profile')
professional_api.add_resource(GetAvailableServices, '/professional/services')
professional_api.add_resource(ProfessionalSearchAPI, '/professional/search')
professional_api.add_resource(ProfessionalSummaryAPI, '/professional/summary')
