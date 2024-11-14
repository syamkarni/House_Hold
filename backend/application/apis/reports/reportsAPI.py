from flask import send_file
import csv
import io

@reports_bp.route('/reports/export_csv', methods=['POST'])
@auth_required()
@roles_required('admin')
def export_csv():
    try:
        # Fetch closed service requests
        closed_requests = ServiceRequest.query.filter_by(service_status='closed').all()

        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Service ID', 'Customer ID', 'Professional ID', 'Date of Request', 'Remarks'])

        for request in closed_requests:
            writer.writerow([
                request.service_id,
                request.customer_id,
                request.professional_id,
                request.date_of_request,
                request.remarks
            ])

        output.seek(0)

        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            attachment_filename='closed_service_requests.csv'
        )
    except SQLAlchemyError as e:
        return jsonify({'message': 'An error occurred while exporting CSV', 'error': str(e)}), 500
