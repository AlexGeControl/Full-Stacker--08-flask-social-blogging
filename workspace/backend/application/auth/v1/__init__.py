from flask import Blueprint

bp = Blueprint('auth_v1', __name__)

from . import views