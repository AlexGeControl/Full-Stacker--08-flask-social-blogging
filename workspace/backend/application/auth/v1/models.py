from application import db

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

import factory
import factory.fuzzy

import random
from datetime import datetime

#----------------------------------------------------------------------------#
# model
#----------------------------------------------------------------------------#
class Permission:
    NONE = 0
    GET_DRINKS_DETAIL = 1
    POST_DRINKS = 2
    PATCH_DRINKS = 4
    DELETE_DRINKS = 8
    ADMIN = 16


class Role(db.Model):
    # follow the best pratice:
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)

    # role info:
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer, default=Permission.NONE)

    # RBAC:
    users = db.relationship('User', backref='role', lazy=True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = Permission.NONE

    def __repr__(self):
        return '<Role %r>' % self.name

    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    def reset_permission(self):
        self.permissions = Permission.NONE

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permissio(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    @staticmethod
    def init_roles():
        roles = {
            "none": [
                Permission.NONE
            ],
            "user": [
                Permission.GET_DRINKS_DETAIL
            ],
            "admin": [
                Permission.GET_DRINKS_DETAIL,
                Permission.POST_DRINKS,
                Permission.PATCH_DRINKS,
                Permission.DELETE_DRINKS,
                Permission.ADMIN
            ]
        }

        try:
            for name in roles:
                # get role:
                role = Role.query.filter(
                    Role.name == name
                ).first()

                if role is None:
                    role = Role(name = name)
                
                # set permissions:
                role.reset_permission()
                for perm in roles[name]:
                    role.add_permission(perm)
                
                # commit:
                db.session.add(role)
            db.session.commit()
            # on successful db insert, flash a prompt.
            print('[Init Roles]: Done.')
        except:
            db.session.rollback()
            # on unsuccessful db insert, flash an error instead.
            print('[Init Roles]: An error occurred. Cannot init roles for APP.')
        finally:
            db.session.close()


class User(db.Model, UserMixin):
    # follow the best pratice:
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # account info:
    email = db.Column(db.String(64), unique=True, index=True)
    # password digest:
    password_hash = db.Column(db.String(128))
    # RBAC:
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    
    # profile info:
    username = db.Column(db.String(64), unique=True, index=True)
    about_me = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(64), nullable=True)
    member_since = db.Column(db.DateTime, default=datetime.utcnow())
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())

    # posts:
    posts = db.relationship('Post', backref='author', lazy=True)

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
    
    def can(self, perm):
        """ check permissions
        """
        return (self.role is not None) and (self.role.has_permission(perm))
    
    def is_manager(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    """ this will enable direct call of can & is_manager for flask_login current_user
    """
    def can(self, perm):
        """ check permissions
        """
        return False
    
    def is_manager(self):
        return False