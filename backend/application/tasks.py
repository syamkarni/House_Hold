from celery import shared_task
import datetime
import csv
import json
import requests
from .utils import format_report
from .mail import send_email
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
    customers = Customer.query.all()
    for customer in customers:
        if not customer.is_profile_complete():
            continue

        customer_data = {}
        customer_data['name'] = customer.name
        customer_data['email'] = customer.user.u_mail
        customer_data['address'] = customer.address
        customer_data['phone'] = customer.phone

        customer_services = []
        for request in customer.service_requests:
            if request.service_status != "completed":
                continue
            this_service = {
                "service_name": request.service.name if request.service else 'N/A',
                "package_name": request.package.name if request.package else 'N/A',
                "professional_name": request.professional.name if request.professional else 'Not Assigned',
                "date_of_request": str(request.date_of_request),
                "date_of_completion": str(request.date_of_completion) if request.date_of_completion else "Pending",
                "remarks": request.remarks or "",
                "status": request.service_status
            }
            customer_services.append(this_service)

        customer_data['services'] = customer_services

        message = format_report('templates/monthly_report.html', customer_data)
        send_email(
            to_address=customer_data['email'],
            subject="Monthly Report - Household Services",
            message=message,
            content="html"
        )

    return "Monthly reports sent"

@shared_task(ignore_result=False, name="daily_update")
def delivery_report():
    return 'The delivery status is set to user'