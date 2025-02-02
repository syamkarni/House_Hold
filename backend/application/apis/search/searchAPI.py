from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.model import User, Service, ServiceProfessional, Package, ServiceRequest, db
from sqlalchemy.exc import SQLAlchemyError
import datetime

search_bp = Blueprint('search_bp', __name__)
search_api = Api(search_bp)

def serialize_service_request(r):
    service_data = None
    if r.service:
        service_data = {
            'id': r.service.id,
            'name': r.service.name,
            'description': r.service.description,
            'price': r.service.price,
            'time_required': r.service.time_required
        }
    return {
        'id': r.id,
        'service_id': r.service_id,
        'service': service_data,
        'customer_id': r.customer_id,
        'date_of_request': r.date_of_request.isoformat() if r.date_of_request else None,
        'remarks': r.remarks
    }

class SearchAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            identity = get_jwt_identity()
            user_role = identity['roles'][0]
            search_by = request.args.get('search_by')
            search_text = request.args.get('search_text')

            if not search_by:
                return {'message': 'Missing search_by parameter'}, 400

            if search_by != 'date_of_request' and not search_text:
                return {'message': 'Missing search_text parameter'}, 400

            results = []
            if user_role == 'admin':
                results = self.admin_search(search_by, search_text)
            elif user_role == 'professional':
                results = self.professional_search(search_by, search_text)
            elif user_role == 'customer':
                results = self.customer_search(search_by, search_text)
            else:
                return {'message': 'Invalid role'}, 403

            if not results:
                return {'message': 'No results found', 'results': []}, 200

            return {'results': results}, 200
        except SQLAlchemyError as e:
            return {'message': 'Error during search', 'error': str(e)}, 500

    def admin_search(self, search_by, search_text):
        if search_by == 'customer':
            customers = User.query.join(User.customer).filter(
                User.u_mail.ilike(f"%{search_text}%") | User.customer.name.ilike(f"%{search_text}%")
            ).all()
            return [{'id': user.user_id, 'email': user.u_mail, 'name': user.customer.name} for user in customers]

        elif search_by == 'professional':
            professionals = ServiceProfessional.query.filter(
                ServiceProfessional.name.ilike(f"%{search_text}%")
            ).all()
            return [{'id': prof.id, 'name': prof.name, 'service': prof.service.name if prof.service else None} for prof in professionals]

        elif search_by == 'service':
            services = Service.query.filter(Service.name.ilike(f"%{search_text}%")).all()
            return [{'id': svc.id, 'name': svc.name, 'description': svc.description} for svc in services]
        else:
            return []

    def professional_search(self, search_by, search_text):
        if search_by == 'service':
            services = Service.query.filter(Service.name.ilike(f"%{search_text}%")).all()
            return [{'id': svc.id, 'name': svc.name, 'description': svc.description} for svc in services]

        elif search_by == 'date_of_request':
            date_from = request.args.get('date_from')
            date_to = request.args.get('date_to')
            query = ServiceRequest.query
            try:
                if date_from:
                    date_from_obj = datetime.datetime.strptime(date_from, "%Y-%m-%d")
                    query = query.filter(ServiceRequest.date_of_request >= date_from_obj)
                if date_to:
                    date_to_obj = datetime.datetime.strptime(date_to, "%Y-%m-%d")
                    query = query.filter(ServiceRequest.date_of_request <= date_to_obj)
                results = query.all()
                return [serialize_service_request(r) for r in results]
            except ValueError as e:
                return {'message': 'Invalid date format. Use YYYY-MM-DD', 'error': str(e)}, 400

        elif search_by == 'customer_remarks':
            results = ServiceRequest.query.filter(ServiceRequest.remarks.ilike(f"%{search_text}%")).all()
            return [serialize_service_request(r) for r in results]
        else:
            return []

    def customer_search(self, search_by, search_text):
        if search_by == 'services':
            services = Service.query.filter(Service.name.ilike(f"%{search_text}%")).all()
            return [{'id': svc.id, 'name': svc.name, 'description': svc.description} for svc in services]

        elif search_by == 'packages':
            packages = Package.query.filter(Package.name.ilike(f"%{search_text}%")).all()
            return [{'id': pkg.id, 'name': pkg.name, 'description': pkg.description} for pkg in packages]
        else:
            return []

search_api.add_resource(SearchAPI, '/search')
