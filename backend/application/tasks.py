from celery import shared_task
from collections import defaultdict
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


@shared_task(ignore_result=False, name="daily_reminder")
def daily_reminder():
    """
    1) Email the admin about any professionals needing approval.
    2) Email each professional who has requested (not yet accepted/rejected) service requests.
    """

    #####################################
    # PART A) Admin Reminder
    #####################################
    # For simplicity, assume there's exactly one admin with role='admin'
    admin_user = User.query.join(User.roles).filter_by(name='admin').first()
    admin_email = admin_user.u_mail if admin_user else None

    # Find unapproved professionals
    pending_professionals = ServiceProfessional.query.filter_by(approved=False).all()
    pending_count = len(pending_professionals)

    if admin_email and pending_count > 0:
        # Prepare data to render the email template
        admin_context = {
            "pending_count": pending_count,
            "pending_list": [prof.name for prof in pending_professionals],  # or any extra data
        }
        # Render HTML template
        rendered_admin_email = format_report('templates/daily_reminder_admin.html', admin_context)

        # Send the email
        send_email(
            to_address=admin_email,
            subject="Daily Reminder: Approvals Pending",
            message=rendered_admin_email,
            content="html"
        )

    #####################################
    # PART B) Professional Reminders
    #####################################
    requests = ServiceRequest.query.filter_by(service_status='requested').all()

    # Group requests by the assigned professional
    pro_map = defaultdict(list)
    for req in requests:
        if req.professional:
            pro_map[req.professional].append(req)

    # For each professional, build & send an email listing their pending requests
    for professional, req_list in pro_map.items():
        if professional.is_blocked or not professional.approved:
            # Skip blocked or not-yet-approved professionals
            continue

        prof_user = professional.user
        if not prof_user or not prof_user.u_mail:
            continue

        # Build the context for the professional
        context = {
            "professional_name": professional.name,
            "requests_count": len(req_list),
            "requests": req_list,  # We'll loop over them in the template
        }
        # Render the HTML
        rendered_prof_email = format_report('templates/daily_reminder_professional.html', context)

        # Send the email
        send_email(
            to_address=prof_user.u_mail,
            subject="Daily Reminder: You Have Pending Requests",
            message=rendered_prof_email,
            content="html"
        )

    return "Daily reminders sent successfully!"



# @shared_task(ignore_result=False, name="daily_update")
# def delivery_report():

#     #https://chat.googleapis.com/v1/spaces/AAAAejlaOJg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=O4X2zRmxL9q2fFueEi1ySro61SvjWPgn5qmDLyV92mI
#     return 'The delivery status is set to user'




# @shared_task(name="notify_professional_approval")
# def notify_professional_approval(prof_email, is_approved):
#     """
#     Sends a Google Chat (or other) notification that the professional's profile
#     was just approved or rejected.
#     """
#     if is_approved:
#         text = f"Congratulations! Your professional profile ({prof_email}) is now approved."
#     else:
#         text = f"Sorry, your professional profile ({prof_email}) has been rejected by the admin."

#     chat_webhook = "https://chat.googleapis.com/v1/spaces/AAAAsample/messages?key=YOURKEY&token=YOURTOKEN"
#     payload = {"text": text}
#     try:
#         response = requests.post(chat_webhook, json=payload, timeout=10)
#         response.raise_for_status()
#         return f"Notification sent to {prof_email} with status code {response.status_code}"
#     except requests.RequestException as e:
#         return f"Failed to send notification to {prof_email}: {e}"



from celery import shared_task
import requests

@shared_task(name="notify_customer_action")
def notify_customer_action(email, action_type, extra_info=None):
    """
    Notifies the customer that they have performed a certain action:
      - close_service_request
      - cancel_service_request
      - provide_review
    'extra_info' can be any additional data you want to display.
    """
    # Build the message text
    text = f"Hello {email}, you have just performed the action: {action_type}.\n"
    if extra_info:
        text += f"Details: {extra_info}\n"
    text += "Thanks for using our platform!"

    # Example: Send to Google Chat (replace with your actual webhook)
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAejlaOJg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=O4X2zRmxL9q2fFueEi1ySro61SvjWPgn5qmDLyV92mI"
    payload = {"text": text}

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        return f"Notification sent to {email}, status={response.status_code}"
    except requests.RequestException as e:
        return f"Failed to notify {email}: {e}"

