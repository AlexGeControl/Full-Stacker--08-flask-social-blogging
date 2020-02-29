from application import db

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import factory
import factory.fuzzy

import random

#----------------------------------------------------------------------------#
# model
#----------------------------------------------------------------------------#
class Role(db.Model):
    # follow the best pratice:
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)

    # role info:
    name = db.Column(db.String(64), unique=True)

    # RBAC:
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model, UserMixin):
    # follow the best pratice:
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # account info:
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)

    # password digest:
    password_hash = db.Column(db.String(128))

    # RBAC:
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    
    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        """ password getter
        """
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """ password setter
        """
        # save password digest only:
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """ verify password
        """
        return check_password_hash(self.password_hash, password)