import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
from flask_caching import Cache
from flask_mail import Mail
from application.data.model import db, User, Role
from application.cache import cache
from application.security import user_datastore
from application.apis import api_blueprints
from application.tasks import make_celery
import application.config as config



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SECURITY_REGISTERABLE'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SECURITY_PASSWORD_SALT'] = config.SECURITY_PASSWORD_SALT
app.config['CELERY_BROKER_URL'] = config.CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = config.CELERY_RESULT_BACKEND


db.init_app(app)

migrate = Migrate(app, db)
security = Security(app, user_datastore)
jwt = JWTManager(app)


CORS(app)
cache.init_app(app)

mail = Mail(app)
celery = make_celery(app)



for bp in api_blueprints:
    app.register_blueprint(bp)

@app.route("/")
def index():
    return {
        "message": "Welcome to the Household Services API!",
        "endpoints": {
            "Register User": "/register (POST)",
            "Login User": "/login (POST)",
            "Refresh Token": "/refresh (POST)",
            "Create Service Request": "/customer/service_request (POST)",
            "View Service Requests": "/customer/service_requests (GET)"
        }
    }



if __name__ == '__main__':
    app.run(debug=True)
