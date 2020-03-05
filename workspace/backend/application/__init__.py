from flask import Flask

from flask_cors import CORS
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

from config import basedir, config
import logging
from .utils import format_datetime, create_file_handler

cors = CORS()
db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()
pagedown = PageDown()

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
    # a. user loader for session management:
    @login_manager.user_loader
    def load_user(user_id):
        from application.auth.models import User

        # parse user id from input unicode identifier
        user_id = int(user_id)
        
        return User.query.get(user_id)
    # b. endpoint for login view:
    login_manager.login_view = 'auth.login'
    # c. default current_user:
    from application.auth.models import AnonymousUser
    login_manager.anonymous_user = AnonymousUser

    # enable SQLAlchemy:
    db.init_app(app)
    # enable moment:
    moment.init_app(app)
    # enable markdown editor:
    pagedown.init_app(app)

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

    from .posts import bp as blueprint_posts
    app.register_blueprint(blueprint_posts, url_prefix='/posts')
    
    #  apis
    #  ----------------------------------------------------------------  

    return app

from . import models