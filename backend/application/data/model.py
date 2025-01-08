from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
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

    customer = db.relationship('Customer', back_populates='user', uselist=False)
    service_professional = db.relationship('ServiceProfessional', back_populates='user', uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

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
    name = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    is_blocked = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='customer')
    service_requests = db.relationship('ServiceRequest', back_populates='customer')
    reviews = db.relationship('Review', back_populates='customer')

    def is_profile_complete(self):
        return bool(self.name and self.phone and self.address)

class ServiceProfessional(db.Model):
    __tablename__ = 'service_professional'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    description = db.Column(db.Text)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    experience = db.Column(db.Integer)
    approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='service_professional')
    service = db.relationship('Service', back_populates='professionals') 
    service_requests = db.relationship('ServiceRequest', back_populates='professional')
    reviews = db.relationship('Review', back_populates='professional')

    def is_profile_complete(self):
        return bool(self.name and self.description and self.service_id and self.experience)

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer)
    description = db.Column(db.Text)

    professionals = db.relationship('ServiceProfessional', back_populates='service')  
    service_requests = db.relationship('ServiceRequest', back_populates='service')
    packages = db.relationship('Package', back_populates='service', lazy=True)


class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer)  

    service = db.relationship('Service', back_populates='packages')


class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(50), default='requested')
    remarks = db.Column(db.Text)

    service = db.relationship('Service', back_populates='service_requests')
    package = db.relationship('Package')
    customer = db.relationship('Customer', back_populates='service_requests')
    professional = db.relationship('ServiceProfessional', back_populates='service_requests')
    reviews = db.relationship('Review', back_populates='service_request')

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    service_request = db.relationship('ServiceRequest', back_populates='reviews')
    customer = db.relationship('Customer', back_populates='reviews')
    professional = db.relationship('ServiceProfessional', back_populates='reviews')
