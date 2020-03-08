from flask import Flask

from flask_cors import CORS
from flask_login import LoginManager
from flask_moment import Moment
from authlib.integrations.flask_client import OAuth
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
    # config login manager for auth/v1:
    login_manager.init_app(app)
    # a. user loader for session management:
    @login_manager.user_loader
    def load_user(user_id):
        from application.auth.v1.models import User

        # parse user id from input unicode identifier
        user_id = int(user_id)
        
        return User.query.get(user_id)
    # b. endpoint for login view:
    login_manager.login_view = 'auth_v1.login'
    # c. default current_user:
    from application.auth.v1.models import AnonymousUser
    login_manager.anonymous_user = AnonymousUser

    # config Auth0 for auth/v2:
    def fetch_token(name):
        token = OAuth2Token.find(
            name=name,
            user="udasocialblogging",
        )
        return token.to_token()

    from authlib.integrations.flask_client import token_update
    @token_update.connect_via(app)
    def on_token_update(sender, name, token, refresh_token=None, access_token=None):
        if refresh_token:
            item = OAuth2Token.find(name=name, refresh_token=refresh_token)
        elif access_token:
            item = OAuth2Token.find(name=name, access_token=access_token)
        else:
            return

        # update old token
        item.access_token = token['access_token']
        item.refresh_token = token.get('refresh_token')
        item.expires_at = token['expires_at']
        item.save()

    oauth = OAuth(fetch_token=fetch_token)
    oauth.init_app(app)

    app.config['AUTH0'] = oauth.register(
        'auth0',
        client_id = app.config['AUTH0_CLIENT_ID'],
        client_secret = app.config['AUTH0_CLIENT_SECRET'],
        api_base_url = app.config['AUTH0_DOMAIN_URL'],
        access_token_url = app.config['AUTH0_ACCESS_TOKEN_URL'],
        authorize_url = app.config['AUTH0_AUTHORIZE_URL'],
        client_kwargs={
            'scope': app.config['AUTH0_SCOPE'],
        },
    )

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
    from .auth.v1 import bp as blueprint_auth_v1
    app.register_blueprint(blueprint_auth_v1, url_prefix='/auth/v1')
    from .auth.v2 import bp as blueprint_auth_v2
    app.register_blueprint(blueprint_auth_v2, url_prefix='/auth/v2')

    #  views
    #  ----------------------------------------------------------------    
    from .main import bp as blueprint_main
    app.register_blueprint(blueprint_main)

    from .users import bp as blueprint_users
    app.register_blueprint(blueprint_users, url_prefix='/users')

    from .posts import bp as blueprint_posts
    app.register_blueprint(blueprint_posts, url_prefix='/posts')

    from .follows import bp as blueprint_follows
    app.register_blueprint(blueprint_follows, url_prefix='/follows')

    #  apis
    #  ----------------------------------------------------------------  
    from .api.v2 import bp as blueprint_api 
    app.register_blueprint(blueprint_api, url_prefix='/api/v2')

    return app

from . import models