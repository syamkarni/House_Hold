from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.model import ServiceRequest, db
from sqlalchemy.exc import SQLAlchemyError
import csv
import io
import datetime

reports_bp = Blueprint('reports_bp', __name__)
reports_api = Api(reports_bp)

class ExportCSV(Resource):
    @jwt_required()
    def post(self):
        try:
            identity = get_jwt_identity()
            roles = identity['roles']

            if 'admin' not in roles:
                return {'message': 'Admins only'}, 403

            # Optional date filters
            data = request.get_json()
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            query = ServiceRequest.query.filter_by(service_status='closed')

            if start_date:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(ServiceRequest.date_of_completion >= start_date)
            if end_date:
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                query = query.filter(ServiceRequest.date_of_completion <= end_date)

            closed_requests = query.all()

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Service ID', 'Customer ID', 'Professional ID', 'Date of Request', 'Date of Completion', 'Remarks'])

            for request in closed_requests:
                writer.writerow([
                    request.service_id,
                    request.customer_id,
                    request.professional_id,
                    request.date_of_request.isoformat(),
                    request.date_of_completion.isoformat() if request.date_of_completion else '',
                    request.remarks
                ])

            output.seek(0)

            return (
                output.getvalue(),
                200,
                {
                    'Content-Type': 'text/csv',
                    'Content-Disposition': 'attachment; filename="closed_service_requests.csv"'
                }
            )
        except SQLAlchemyError as e:
            return {'message': 'An error occurred while exporting CSV', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500


reports_api.add_resource(ExportCSV, '/reports/export_csv')
