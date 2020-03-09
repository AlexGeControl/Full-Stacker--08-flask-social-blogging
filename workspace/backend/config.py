import os

# root dir of app:
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # enable auth0 callback:
    # SERVER_NAME = '0.0.0.0'

    # security:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

    # ssl: 
    SSL_REDIRECT = False

    # database:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # auth0 authentication:
    AUTH0 = None
    AUTH0_ALGORITHMS = ['RS256']
    AUTH0_DOMAIN_URL = 'https://dev-d-and-g-udasocialblogging.auth0.com/'
    AUTH0_AUDIENCE = 'dev-d-and-g-udasocialblogging-api'
     # TODO: this must be provided as environment variable
    AUTH0_MANAGEMENT_TOKEN = os.environ.get('AUTH0_MANAGEMENT_TOKEN')
    AUTH0_CLIENT_ID = 'i7QHAQjPi6oU1LLFFlU0rlI0q46H3nok'
    # TODO: this must be provided as environment variable
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_DB_CONNECTION = 'Username-Password-Authentication'
    AUTH0_ACCESS_TOKEN_URL = 'https://dev-d-and-g-udasocialblogging.auth0.com/oauth/token'
    AUTH0_AUTHORIZE_URL = 'https://dev-d-and-g-udasocialblogging.auth0.com/authorize'
    AUTH0_LOGOUT_URL = 'https://dev-d-and-g-udasocialblogging.auth0.com/v2/logout'
    AUTH0_SCOPE = 'openid profile email updated_at'

    # posts:
    POSTS_PER_PAGE = 15
    # follows:
    FOLLOWS_PER_PAGE = 15
    
    # mail service:
    """
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    """

    @staticmethod
    def init_app(app):
        """ integrate with app factory
        """
        pass

class DevelopmentConfig(Config):
    DEBUG = True

    # sqlite:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #   'sqlite:///' + os.path.join(basedir, 'database', 'database.db')

    # pgsql:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
       'postgres://jymqfwebhbhmqo:2e3b7278bd5ac51d89edbad6630ee2ece644d47a9e5f2b979c46723e982a2c44@ec2-50-17-178-87.compute-1.amazonaws.com:5432/d2fk3rfellliga'

class TestingConfig(Config):
    TESTING = True

    # enable request in test cases:
    SERVER_NAME = 'localhost.localdomain'

    # JWT token:
    AUTH0_ROLE_NONE = ""
    AUTH0_ROLE_USER = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rUTVOVEZDTXpaRk5UYzFPVVk1T0VVMlF6VXdPRFExUVRFME56UkRRek14T0VGRE1UVkdSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1kLWFuZC1nLXVkYXNvY2lhbGJsb2dnaW5nLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTYzMGRiYTEwYjQ2MTBkM2Q4OTZjNjgiLCJhdWQiOiJkZXYtZC1hbmQtZy11ZGFzb2NpYWxibG9nZ2luZy1hcGkiLCJpYXQiOjE1ODM2NzY0MzcsImV4cCI6MTU4MzY4MzYzNywiYXpwIjoiaTdRSEFRalBpNm9VMUxMRkZsVTBybEkwcTQ2SDNub2siLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwb3N0LWRldGFpbCIsInBhdGNoOnBvc3QiLCJwb3N0OnBvc3QiXX0.kV9oOvAb3lL00bAqEkWE4hWcudAD75a4_LNJrS-jjZLGQjOPqYenuE8Y6LL-HU4XUcVqRlGfwEbH1D-TjajCTn55iW2iu-fRvNoLVw3LIMUYC_76dlh4ywuEItmYPReYxxH9knnfAR7hYK7H_FKemhsjiTC-5jyVy941MFOxBYS3fN6N2w5RFifOLq6en1EkqexCISKIiUVolGwlwgByS0yOmu4EDqLdhy85Z9RXPSXyvPvOEIuZalFuZSJUvtDQP0q0ZNpOuFhN8Kh9fexNY9_ubkSoHjNMuaB8V_jJavld8dvehTyGBD-9_GcXnQMa-q5WYDmrK0_1qk5LE9do-g"
    AUTH0_ROLE_ADMIN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rUTVOVEZDTXpaRk5UYzFPVVk1T0VVMlF6VXdPRFExUVRFME56UkRRek14T0VGRE1UVkdSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1kLWFuZC1nLXVkYXNvY2lhbGJsb2dnaW5nLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTYzMDVhMDEwYjQ2MTBkM2Q4OTVjZDQiLCJhdWQiOiJkZXYtZC1hbmQtZy11ZGFzb2NpYWxibG9nZ2luZy1hcGkiLCJpYXQiOjE1ODM2NzYzMzMsImV4cCI6MTU4MzY4MzUzMywiYXpwIjoiaTdRSEFRalBpNm9VMUxMRkZsVTBybEkwcTQ2SDNub2siLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkbWluOmFsbCIsImRlbGV0ZTpwb3N0IiwiZ2V0OnBvc3QtZGV0YWlsIiwicGF0Y2g6cG9zdCIsInBvc3Q6cG9zdCJdfQ.DS_IrbaiBX0VqwemUkZUXDd6-QhbAELuZR1nTxZnLRYqcaUG8OIC_5I4BMQIPXjdGWEQ_Gr4Iut2RD9lEAXnkrbshyx2lUu1MiGPM5LCsK71iQCtxIyOC16cNnbjWMT_NRvgQsSR5tTZ43DgF24mf7lfz8b4VL-sJSxsAzpNKs4hTYF1Xz9NzYIEy9drHnr5a0If-QifcHoz4FKl_fVCO_Izww0XFCX7bCSUEQN9Y-egQlSoFTpPB-XFRWLjCMprmPaK3Y7tuFz4uON19z2rXmEqIQkCl4cRKm0-ExqmBufsYihYAXCMqHQIzBILZR-PQNXtU4RXU2m08_3H9Xv75g"

    # database:
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgresql://udacity:udacity@db:5432/udasocialbloggingapptest'

class ProductionConfig(Config):
    # sqlite:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'todos.sqlite')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://jymqfwebhbhmqo:2e3b7278bd5ac51d89edbad6630ee2ece644d47a9e5f2b979c46723e982a2c44@ec2-50-17-178-87.compute-1.amazonaws.com:5432/d2fk3rfellliga'

class HerokuConfig(Config):
    # ssl:
    SSL_REDIRECT = True if os.environ.get('DYNO') else False
    
    # use heroku pg instance:    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    @staticmethod
    def init_app(app):
        """ specific init for heroku 
        """
        # enable heroku logs
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # handle reverse proxy server headers        
        from werkzeug.contrib.fixers import ProxyFix        
        app.wsgi_app = ProxyFix(app.wsgi_app)

# configs:
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}