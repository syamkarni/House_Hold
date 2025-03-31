from celery import shared_task
import datetime
import csv
import json
from application.data.model import *

@shared_task(ignore_result=False, name="download_csv_report")
def csv_report():
    # time.sleep(16)  
    csv_file_name=f"transation_{datetime.datetime.now().strftime('%f')}.csv"
    with open(f'static/{csv_file_name}', 'w', newline="") as csvfile:
        sr_no = 1
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([
            'Sr No.', 
            'Service Name',
            'Package Name', 
            'Customer Name', 
            'Professional Name', 
            'Date of Request', 
            'Date of Completion', 
            'Service Status', 
            'Remarks'
        ])
        service_requests = ServiceRequest.query.all()

        for req in service_requests:
            writer.writerow([
                sr_no,
                req.service.name if req.service else 'N/A',
                req.package.name if req.package else 'N/A',
                req.customer.name if req.customer else 'N/A',
                req.professional.name if req.professional else 'Not Assigned',
                req.date_of_request,
                req.date_of_completion if req.date_of_completion else 'Pending',
                req.service_status,
                req.remarks if req.remarks else ''
            ])
            sr_no += 1

    return csv_file_name
    
    
    # return 'Initiated csv download'

@shared_task(ignore_result=False, name="monthly_report")
def monthly_report():
    return 'monthly report sent'

@shared_task(ignore_result=False, name="daily_update")
def delivery_report():
    return 'The delivery status is set to user'