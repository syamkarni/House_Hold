from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required
from ...data.model import User, ServiceProfessional, Service, db
from sqlalchemy.exc import SQLAlchemyError

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin/professional/<int:professional_id>/approve', methods=['PUT'])
@auth_required()
@roles_required('admin')
def approve_professional(professional_id):
    try:
        professional = ServiceProfessional.query.get_or_404(professional_id)
        if professional.approved:
            return jsonify({'message': 'Professional is already approved'}), 400

        professional.approved = True
        db.session.commit()
        return jsonify({'message': 'Service professional approved successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while approving professional', 'error': str(e)}), 500


@admin_bp.route('/admin/user/<int:user_id>/block', methods=['PUT'])
@auth_required()
@roles_required('admin')
def block_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        user.active = False


        if user.customer:
            user.customer.is_blocked = True

        if user.service_professional:
            user.service_professional.is_blocked = True

        db.session.commit()
        return jsonify({'message': 'User blocked successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while blocking user', 'error': str(e)}), 500


@admin_bp.route('/admin/user/<int:user_id>/unblock', methods=['PUT'])
@auth_required()
@roles_required('admin')
def unblock_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        user.active = True

        if user.customer:
            user.customer.is_blocked = False

        if user.service_professional:
            user.service_professional.is_blocked = False

        db.session.commit()
        return jsonify({'message': 'User unblocked successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while unblocking user', 'error': str(e)}), 500


@admin_bp.route('/admin/service', methods=['POST'])
@auth_required()
@roles_required('admin')
def create_service():
    data = request.get_json()
    try:
        name = data['name']
        price = data['price']
        time_required = data.get('time_required')
        description = data.get('description')


        if Service.query.filter_by(name=name).first():
            return jsonify({'message': 'Service already exists'}), 400

        new_service = Service(
            name=name,
            price=price,
            time_required=time_required,
            description=description
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify({'message': 'Service created successfully', 'service_id': new_service.id}), 201
    except KeyError as e:
        return jsonify({'message': f'Missing required field: {e}'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while creating service', 'error': str(e)}), 500
    

@admin_bp.route('/admin/service/<int:service_id>', methods=['PUT'])
@auth_required()
@roles_required('admin')
def update_service(service_id):
    data = request.get_json()
    try:
        service = Service.query.get_or_404(service_id)
        service.name = data.get('name', service.name)
        service.price = data.get('price', service.price)
        service.time_required = data.get('time_required', service.time_required)
        service.description = data.get('description', service.description)

        db.session.commit()
        return jsonify({'message': 'Service updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while updating service', 'error': str(e)}), 500

@admin_bp.route('/admin/service/<int:service_id>', methods=['DELETE'])
@auth_required()
@roles_required('admin')
def delete_service(service_id):
    try:
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting service', 'error': str(e)}), 500
