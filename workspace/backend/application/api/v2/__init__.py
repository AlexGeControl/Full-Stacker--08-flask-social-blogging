from flask import Blueprint

bp = Blueprint('api_v2', __name__)

from . import errors, drinks