from flask import Blueprint

bp = Blueprint('auth_v2', __name__)

from .services import Users
service_user_management = Users()

from . import views