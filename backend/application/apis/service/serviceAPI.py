from flask import Blueprint, jsonify
from flask_restful import Resource, Api
from application.data.model import Service
from sqlalchemy.exc import SQLAlchemyError

service_bp = Blueprint('service_bp', __name__)
service_api = Api(service_bp)

class ListServices(Resource):
    def get(self):
        try:
            services = Service.query.all()
            service_list = [{
                'id': s.id,
                'name': s.name,
                'price': s.price,
                'time_required': s.time_required,
                'description': s.description
            } for s in services]
            return {'services': service_list}, 200
        except SQLAlchemyError as e:
            return {'message': 'An error occurred while fetching services', 'error': str(e)}, 500

class GetService(Resource):
    def get(self, service_id):
        try:
            service = Service.query.get_or_404(service_id)
            service_data = {
                'id': service.id,
                'name': service.name,
                'price': service.price,
                'time_required': service.time_required,
                'description': service.description
            }
            return {'service': service_data}, 200
        except SQLAlchemyError as e:
            return {'message': 'An error occurred while fetching service', 'error': str(e)}, 500


service_api.add_resource(ListServices, '/services')
service_api.add_resource(GetService, '/services/<int:service_id>')
