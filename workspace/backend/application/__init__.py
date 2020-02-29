from flask import Flask

from flask_cors import CORS
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import basedir, config
import logging
from .utils import format_datetime, create_file_handler

cors = CORS()
db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()

def create_app(config_name):
    app = Flask(
        __name__,
        static_url_path = '/static', static_folder = 'static'
    )
    # load configs:
    app.config.from_object(config[config_name])    
    config[config_name].init_app(app)    
    
    # enable CORS:
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    """
    # config login manager:
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from application.auth.models import User

        # parse user id from input unicode identifier
        user_id = int(user_id)
        
        return User.query.get(user_id)
    
    login_manager.login_view = 'auth.login'

    from application.auth.models import AnonymousUser
    login_manager.anonymous_user = AnonymousUser

    # enable SQLAlchemy:
    db.init_app(app)
    # enable moment:
    moment.init_app(app)

    # jinja:
    app.jinja_env.filters['datetime'] = format_datetime
    # logging:
    app.logger.setLevel(logging.INFO)
    app.logger.info('errors')
    app.logger.addHandler(create_file_handler(basedir))

    # attach routes and custom error pages here

    #  errors
    #  ----------------------------------------------------------------
    from .errors import register_error_handlers
    register_error_handlers(app)
    
    #  auth
    #  ----------------------------------------------------------------  
    from .auth import bp as blueprint_auth
    app.register_blueprint(blueprint_auth, url_prefix='/auth')

    #  views
    #  ----------------------------------------------------------------    
    from .main import bp as blueprint_main
    app.register_blueprint(blueprint_main)

    from .drinks import bp as blueprint_drinks
    app.register_blueprint(blueprint_drinks, url_prefix='/drinks')
    
    #  apis
    #  ----------------------------------------------------------------  
    from .api.v1 import bp as blueprint_api_v1
    app.register_blueprint(blueprint_api_v1, url_prefix='/api/v1')

    from .api.v2 import bp as blueprint_api_v2
    app.register_blueprint(blueprint_api_v2, url_prefix='/api/v2')

    return app

from . import models