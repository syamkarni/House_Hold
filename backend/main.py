import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from flask_mail import Mail
from application.data.model import db
from application.cache import cache
from application.apis import api_blueprints
from application.tasks import make_celery
import application.config as config
from flask import jsonify


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
celery = make_celery(app)





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

if __name__ == '__main__':
    app.run(debug=True)
