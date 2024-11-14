from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from ...data.model import ServiceRequest, db
from sqlalchemy.exc import SQLAlchemyError
import datetime

professional_bp = Blueprint('professional_bp', __name__)

@professional_bp.route('/professional/service_requests', methods=['GET'])
@auth_required()
@roles_required('professional')
def list_assigned_service_requests():
    try:
        requests=ServiceRequest.query.filter_by(professional_id=current_user.service_professional.id).all()
        request_list = [{
            'id': r.id,
            'service_id': r.service_id,
            'customer_id': r.customer_id,
            'date_of_request': r.date_of_request,
            'service_status': r.service_status,
            'remarks': r.remarks
        } for r in requests]

        return jsonify({'requests': request_list}), 200
    except SQLAlchemyError as e:
        return jsonify({'message': 'An error occurred while fetching service requests', 'error': str(e)}), 500
    
@professional_bp.route('/professional/service_request/<int:request_id>/accept', methods=['PUT'])
@auth_required()
@roles_required('professional')
def accept_service_request(request_id):
    try:
        service_request=ServiceRequest.query.get_or_404(request_id)
        if service_request.service_status != 'assigned':
            return jsonify({'message': 'Service request is not assigned yet'}), 400
        service_request.professional_id=current_user.service_professional.id
        service_request.service_status='assigned'
        db.session.commit()
        return jsonify({'message': 'Service request accepted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while accepting service request', 'error': str(e)}), 500
    
    
@professional_bp.route('/professional/service_request/<int:request_id>/reject', methods=['PUT'])
@auth_required()
@roles_required('professional')
def reject_service_request(request_id):
    try:
        service_request=ServiceRequest.query.get_or_404(request_id)
        if service_request.service_status!='requested':
            return jsonify({'message': 'Service request cannot be rejected'}), 400
        service_request.service_status='rejected'
        db.session.commit()
        return jsonify({'message': 'Service request rejected successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while rejecting service request', 'error': str(e)}), 500
    
@professional_bp.route('/professional/service_request/<int:request_id>/complete', methods=['PUT'])
@auth_required()
@roles_required('professional')
def complete_service_request(request_id):
    try:
        service_request=ServiceRequest.query.get_or_404(request_id)
        if service_request.professional_id!=current_user.service_professional.id:
            return jsonify({'message': 'Unauthorised access to complete service request'}), 403
        if service_request.service_status!='assigned':
            return jsonify({'message': 'Only assigned requests can be marked as completed'}), 400
        
        service_request.service_status='completed'
        service_request.date_of_completion=datetime.datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Service request completed successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while completing service request', 'error': str(e)}), 500