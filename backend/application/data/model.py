from .database import db
from flask_security.utils import verify_password, hash_password
import datetime

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    users = db.relationship('User', secondary='user_role', backref=db.backref('roles', lazy='dynamic'))

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    u_mail = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    customer = db.relationship('Customer', backref='user', uselist=False)
    service_professional = db.relationship('ServiceProfessional', backref='user', uselist=False)

    # Add methods for password hashing and verification
    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        is_valid = verify_password(self.password, password)
        print(f"Checking password: {password}")
        print(f"Stored hash: {self.password}")
        print(f"Password valid: {is_valid}")
        return is_valid

    def get_roles(self):
        return [role.name for role in self.roles]

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    is_blocked = db.Column(db.Boolean, default=False)

    service_requests = db.relationship('ServiceRequest', backref='customer')

class ServiceProfessional(db.Model):
    __tablename__ = 'service_professional'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    description = db.Column(db.Text)
    service_type = db.Column(db.String(255))
    experience = db.Column(db.Integer)
    approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)

    service_requests = db.relationship('ServiceRequest', backref='professional')

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer)
    description = db.Column(db.Text)

    service_requests = db.relationship('ServiceRequest', backref='service')

class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(50), default='requested')  # e.g., requested, assigned, closed
    remarks = db.Column(db.Text)

    reviews = db.relationship('Review', backref='service_request')

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    customer = db.relationship('Customer', backref='reviews')
    professional = db.relationship('ServiceProfessional', backref='reviews')
