SQLALCHEMY_DATABASE_URI = 'sqlite:///../db_directory/flaskblog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'your_secret_key'  # need to set this #incomplete
SECURITY_PASSWORD_SALT= 'salt'

#celeryy config here
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'