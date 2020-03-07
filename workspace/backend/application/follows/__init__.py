from flask import Blueprint

bp = Blueprint('follows', __name__)

from . import views