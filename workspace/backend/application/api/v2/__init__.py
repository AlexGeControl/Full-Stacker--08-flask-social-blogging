from flask import Blueprint
from flask_restplus import Api

from config import config

bp = Blueprint('api_v2', __name__)

api = Api(bp, 
    version='1.0', 
    title='Uda Social Blogging API',
    description='API doc for Uda Social Blogging, version 1.0'
)

from .posts import ns as ns_posts
api.add_namespace(ns_posts)

from . import errors
