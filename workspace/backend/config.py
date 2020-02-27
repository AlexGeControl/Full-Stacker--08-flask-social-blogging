import os

# root dir of app:
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # security:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    # database:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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
       'postgresql://udacity:udacity@db:5432/udaspicelatteapp'

class TestingConfig(Config):
    TESTING = True

    # enable request in test cases:
    SERVER_NAME = 'localhost.localdomain'

    # database:
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    # sqlite:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'todos.sqlite')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://udacity:udacity@db:5432/udaspicelatteapp'

# configs:
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}