from flask import Blueprint

bp = Blueprint('users', __name__)

from application.auth.v2.services import UserByEmail, Users

service_user_by_email = UserByEmail()
service_user_management = Users()

from . import views