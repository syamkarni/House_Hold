import os
from flask import Flask,send_from_directory
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from flask_mail import Mail
from application.data.model import db
from application.cache import cache
from application.apis import api_blueprints
# from application.tasks import make_celery
import application.config as config
from flask import jsonify
from application.celery_init import celery_init_app
from application.tasks import csv_report, monthly_report, daily_reminder
from celery.result import AsyncResult
from celery.schedules import crontab


app = Flask(__name__)
app.config.from_object(config)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

CORS(app)
cache.init_app(app)
mail = Mail(app)
# celery = make_celery(app)
celery=celery_init_app(app)
celery.autodiscover_tasks()





for bp in api_blueprints:
    app.register_blueprint(bp)

@app.route("/")
def index():
    return {
        "message": "Welcome to the Household Services API!",
        "endpoints": {
            "Register User": "/auth/register (POST)",
            "Login User": "/auth/login (POST)",
            "Refresh Token": "/auth/refresh (POST)",
            "Create Service Request": "/customer/service_request (POST)",
            "View Service Requests": "/customer/service_requests (GET)"
        }
    }

@app.route('/report/export') #for triggering
def export_csv():
    result=csv_report.delay()
    return jsonify({
        "id":result.id,
        "result":result.result,
    })

@app.route('/report/csv_result/<id>') #testing purpose only
def csv_result(id):
    result= AsyncResult(id)
    return send_from_directory('static', result.result) if result.ready() else jsonify({
        "message":"The task is still running"
    })
    # return {
    #     'ready':result.ready(),
    #     'successful':result.successful(),
    #     'value':result.result if result.ready() else None,
    # }

@app.route('/api/mail')
def send_reports():
    res = monthly_report.delay()
    return {
        "result": res.result
    }

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(minute = '*/2'),
#         monthly_report.s(),
#     )
# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Executes on the 1st day of every month at 8:00 AM
#     sender.add_periodic_task(
#         crontab(minute=0, hour=8, day_of_month=1),
#         monthly_report.s(),
#     )
#     sender.add_periodic_task(
#         crontab(hour=18, minute=0),
#         daily_reminder.s(),
#     )

# from celery.schedules import schedule

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # every 5 seconds
#     sender.add_periodic_task(
#         schedule(5.0),
#         daily_reminder.s(),
#     )

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=8, day_of_month=1),
        monthly_report.s(),
    )

    sender.add_periodic_task(
        crontab(hour=18, minute=0),
        daily_reminder.s(),
    )

    sender.add_periodic_task(
        schedule(5.0),
        daily_reminder.s(),
    )


if __name__ == '__main__':
    app.run(debug=True)
