from .database import db
from flask_security import UserMixin, RoleMixin
import datetime

class Role(db.Model, RoleMixin):
    __tablename__='role'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), unique=True)
    users=db.relationship('UserRole', backref='role')

class User(db.Model, UserMixin):
    __tablename__='user'
    user_id=db.Column(db.Integer, primary_key=True)
    u_mail=db.Column(db.String(50), unique=True, nullable=False)
    password=db.Column(db.String(255), nullable=False)
    fs_uniquifier=db.Column(db.String(255), nullable=False)
    roles=db.relationship('UserRole', backref='user')
    active=db.Column(db.Boolean, default=True)
    #add accodingly here #incomplete

    def __init__(self, u_mail, password, fs_uniquifier):
        self.u_mail=u_mail
        self.password=password
        self.fs_uniquifier=fs_uniquifier

class UserRole(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'))

#add more schemas here #incomplete