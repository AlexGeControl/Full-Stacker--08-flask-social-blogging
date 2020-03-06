from flask import Blueprint

bp = Blueprint('auth_v2', __name__)

from . import views