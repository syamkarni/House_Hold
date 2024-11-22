SQLALCHEMY_DATABASE_URI = 'sqlite:///../db_directory/flaskblog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'your_secret_key'  # Replace with a secure key
JWT_SECRET_KEY = 'your_jwt_secret_key'

# Flask-Security Configurations
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'your_password_salt'  # Replace with a secure random salt


# Celery Configurations
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'