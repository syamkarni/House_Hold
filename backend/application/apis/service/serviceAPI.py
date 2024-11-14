from flask import Blueprint, jsonify
from ...data.model import Service
from sqlalchemy.exc import SQLAlchemyError

service_bp = Blueprint('service_bp', __name__)

@service_bp.route('/services', methods=['GET'])
def list_services():
    try:
        services=Service.query.all()
        service_list=[{
            'id':s.id,
            'name':s.name,
            'price':s.price,
            'time_required':s.time_required,
            'description':s.description
        } for s in services]
        return jsonify({'services': service_list}), 200
    except SQLAlchemyError as e:
        return jsonify({'message': 'An error occurred while fetching services', 'error': str(e)}), 500


@service_bp.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    try:
        service=Service.query.get_or_404(service_id)
        service_data={
            'id':service.id,
            'name':service.name,
            'price':service.price,
            'time_required':service.time_required,
            'description':service.description
        }
        return jsonify({'service': service_data}), 200
    except SQLAlchemyError as e:
        return jsonify({'message': 'An error occurred while fetching service', 'error': str(e)}), 500