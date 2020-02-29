from flask import Blueprint

bp = Blueprint('drinks', __name__)

from . import views