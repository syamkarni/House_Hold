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
from application.config import Config



app = Flask(__name__)
app.config.from_object(Config)


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


if __name__ == '__main__':
    app.run(debug=True)
