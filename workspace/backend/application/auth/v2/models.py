from application import db

import factory
import factory.fuzzy

import random
from datetime import datetime

#----------------------------------------------------------------------------#
# model
#----------------------------------------------------------------------------#
class DelegatedUser(db.Model):
    # follow the best pratice:
    __tablename__ = 'delegated_users'

    # id:
    id = db.Column(db.String(64), primary_key=True)

    # account info:
    email = db.Column(db.String(64), unique=True, index=True)
    
    # profile info:
    nickname = db.Column(db.String(64), index=True)

    # posts:
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.nickname}>' 