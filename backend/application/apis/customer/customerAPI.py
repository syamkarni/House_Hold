from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from ...data.model import ServiceRequest, db
from sqlalchemy.exc import SQLAlchemyError
import datetime

customer_bp = Blueprint('customer_bp', __name__)


@customer_bp.route('/customer/service_request', methods=['POST'])
@auth_required()
@roles_required('customer')
def create_service_request():
    data=request.get_json()
    try:
        service_id=data['service_id']
        data_of_request=data.get('date_of_request', datetime.datetime.utcnow())
        remarks=data.get('remarks')

        new_request=ServiceRequest(
            service_id=service_id,
            customer_id=current_user.customer.id,
            date_of_request=data_of_request,
            service_status='requested',
            remarks=remarks
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Service request created successfully', 'request_id':new_request.id}), 201

    except KeyError as e:
        return jsonify({'message': 'Missing required data', 'error': str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while creating service request', 'error': str(e)}), 500
    
@customer_bp.route('/customer/serive_request/<int:request_id>', methods=['PUT'])
@auth_required()
@roles_required('customer')
def edit_service_request(request_id):
    data=request.get_json()
    try:
        service_request=ServiceRequest.query.get_or_404(request_id)
        if service_request.customer_id != current_user.customer.id:
            return jsonify({'message': 'Unauthorised access to make a service request'}), 403
        if service_request.service_status not in ['requested', 'assigned']:
            return jsonify({'message': 'Service request cannot be edited'}), 400
        
        service_request.date_of_request=data.get('date_of_request', service_request.date_of_request)
        service_request.remarks= data.get('remarks', service_request.remarks)
        db.session.commit()
        return jsonify({'message': 'Service request updated successfully!'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while updating service request', 'error': str(e)}), 500
    

@customer_bp.route('/customer/service_request/<int:request_id>', methods=['PUT'])
@auth_required
@roles_required('customer')
def close_service_request(request_id):
    try:
        service_request=ServiceRequest.query.get_or_404(request_id)
        if service_request.customer_id!=current_user.customer.id:
            return jsonify({'message': 'Unauthorised access to close service request'}), 403
        if service_request.service_status !='assigned':
            return jsonify({'message': 'Not an assigned request hence cannot be closed'}), 400
        service_request.service_status='closed'
        service_request.date_of_completion=datetime.datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Service request closed successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while closing service request', 'error': str(e)}), 500
    