from .database import db
from flask_security import UserMixin, RoleMixin
import datetime

class Role(db.Model, RoleMixin):
    __tablename__='role'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), unique=True)
    description=db.Column(db.String(255))

    #users=db.relationship('UserRole', backref='role') # add lazy='dynamic' to make it a query ???
    users = db.relationship('User', secondary='user_role', backref=db.backref('roles', lazy='dynamic'))

class User(db.Model, UserMixin):
    __tablename__='user'
    user_id=db.Column(db.Integer, primary_key=True)
    u_mail=db.Column(db.String(50), unique=True, nullable=False)
    password=db.Column(db.String(255), nullable=False)
    fs_uniquifier=db.Column(db.String(255), nullable=False)
    active=db.Column(db.Boolean, default=True)
    confirmed_at=db.Column(db.DateTime, default=datetime.datetime.utcnow)


    roles=db.relationship('UserRole', backref='user')
    customer=db.relationship('Customer', backref='user')
    service_profissional=db.relationship('ServiceProfessional', backref='user')
    #add accodingly here #incomplete

    # def __init__(self, u_mail, password, fs_uniquifier):
    #     self.u_mail=u_mail
    #     self.password=password
    #     self.fs_uniquifier=fs_uniquifier

class UserRole(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'))

class Customer(db.Model):
    __tablename__='customer'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    name=db.Column(db.String(255), nullable=False)
    address=db.Column(db.String(255))
    phone=db.Column(db.String(20))
    is_blocked=db.Column(db.Boolean, default=False)

    service_request=db.relationship('ServiceRequest', backref='customer')

    # def __init__(self, user_id, name, address=None, phone=None):
    #     self.user_id=user_id
    #     self.name=name
    #     self.address=address
    #     self.phone=phone

class ServiceProfessional(db.Model):
    __tablename__='service_profissional'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    name=db.Column(db.String(255), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.datetime.utcnow)
    description=db.Column(db.Text)
    service_type=db.Column(db.String(255))
    experience=db.Column(db.Integer)
    approved=db.Column(db.Boolean, default=False)
    is_blocked=db.Column(db.Boolean, default=False)
    #profile_docs=db.Column(db.String(255)) is this neded(url maybe)? if added:also add it to init #incomplete

    service_request=db.relationship('ServiceRequest', backref='profissional')
    
    # def __init__(self, user_id, name, date_created=None, description=None, service_type=None, experience=None):
    #     self.user_id=user_id
    #     self.name=name
    #     self.date_created=date_created
    #     self.description=description
    #     self.service_type=service_type
    #     self.experience=experience
class Service(db.Model):
    __tablename__='service'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255), nullable=False)
    price=db.Column(db.Float, nullable=False)
    time_required=db.Column(db.Integer)
    description=db.Column(db.Text)

    service_request=db.relationship('ServiceRequest', backref='service')

    # def __init__(self, name, price, time_required=None, description=None):
    #     self.name=name
    #     self.price=price
    #     self.time_required=time_required
    #     self.description=description

class ServiceRequest(db.Model):
    __tablename__='service_request'
    id=db.Column(db.Integer, primary_key=True)
    service_id=db.Column(db.Integer, db.ForeignKey('service.id'))
    customer_id=db.Column(db.Integer, db.ForeignKey('customer.id'))
    professional_id=db.Column(db.Integer, db.ForeignKey('service_profissional.id'), nullable=True)
    date_of_request=db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_of_completion=db.Column(db.DateTime, nullable=True)
    service_status=db.Column(db.String(50), default='requested')  #maybe like requested, assigned, closed
    remarks=db.Column(db.Text)

    review=db.relationship('Review', backref='service_request')

    # def __init__(self, service_id, customer_id, remarks=None):
    #     self.service_id=service_id
    #     self.customer_id=customer_id
    #     self.remarks=remarks
class Review(db.Model):
    __tablename__='review'
    id=db.Column(db.Integer, primary_key=True)
    servie_request_id=db.Column(db.Integer, db.ForeignKey('service_request.id'))
    customer_id=db.Column(db.Integer, db.ForeignKey('customer.id'))
    professional_id=db.Column(db.Integer, db.ForeignKey('service_profissional.id'))
    rating=db.Column(db.Integer, nullable=False)
    comment=db.Column(db.Text)
    date_posted=db.Column(db.DateTime, default=datetime.datetime.utcnow)

    customer=db.relationship('Customer', backref='review')
    professional=db.relationship('ServiceProfessional', backref='review')


    # def __init__(self, service_request_id, customer_id, professional_id, rating, comment):
    #     self.service_request_id=service_request_id
    #     self.customer_id=customer_id
    #     self.professional_id=professional_id
    #     self.rating=rating
    #     self.comment=comment