import os

# root dir of app:
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # enable auth0 callback:
    # SERVER_NAME = '0.0.0.0'

    # security:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

    # database:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # auth0 authentication:
    AUTH0 = None
    AUTH0_ALGORITHMS = ['RS256']
    AUTH0_DOMAIN_URL = 'https://dev-d-and-g-udasocialblogging.auth0.com/'
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
       'postgresql://udacity:udacity@db:5432/udasocialbloggingapp'

class TestingConfig(Config):
    TESTING = True

    # enable request in test cases:
    SERVER_NAME = 'localhost.localdomain'

    # JWT token:
    AUTH0_ROLE_PUBLIC = ""
    AUTH0_ROLE_BARISTA = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qVkZSVGMwUmtJNU1EZzNNVU0wUTBZeU9EQTNPVGswUlVGR01USXlRMFV5TURKQ01VVTVRUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kLWFuZC1nLXVkYXNwaWNlbGF0dGUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNWI5NzA3MzQ5NjNjMGQ0Nzg3ODc0MCIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU4MzEzMjExMiwiZXhwIjoxNTgzMTM5MzEyLCJhenAiOiJab2xYRWw2ZVZDVVFOVThON0J6SWdwcG1kU0lvTGdqNCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.OLvczei0kmidQfmDZrHPcyeVL-vryOMs7TkVFXnySTdnHar8YmHOxMyKs2fBc3-zPyDuej9uQqq7xdiayxDe1oX20Np5fYo_xxfYIvn9YpGMubMw_LTAEyiPRvdwJR-9F-6xtePsYwdsSt_s0H9wmrAlIwF_jzrWbVSEsmQnvIogKolXHdfjjDUWSU4JdNEMagyQAzHOnIWpEAhMT0_ZN20qBtBWYeYsGKjcKIVtAGrnaeyPXG_uDjrSxHrmU0C_diS2ur8WVRWgS-LM9BQUXk4k0y2GodEt-XvLu_ED7j1JXZwQvlbR91Q6pQGlrHLd3rS29D38gSKCwVFVlhZ7Rg"
    AUTH0_ROLE_MANAGER = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qVkZSVGMwUmtJNU1EZzNNVU0wUTBZeU9EQTNPVGswUlVGR01USXlRMFV5TURKQ01VVTVRUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kLWFuZC1nLXVkYXNwaWNlbGF0dGUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNWI5NzhkODgxMTU4MGQ1NzVhMmM3ZSIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU4MzEzMjUxNCwiZXhwIjoxNTgzMTM5NzE0LCJhenAiOiJab2xYRWw2ZVZDVVFOVThON0J6SWdwcG1kU0lvTGdqNCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.rzFnhVJ0V3rmg0Kvu6sqqhpC5WuVedxjMA9b4_DOc6ZytQbEbzVBv4J97IJXJ7gNOyDjCG6bDen0Hnog1iSGEKbfs0zjGP5GedKtY8xzw8rU1pfrnAyo_y9Z4f6d5ZY2ultdLRyJLc1kajP7jkKZ-lp1wVT6E3DXAiJNRwT2GWaew0rknsuc4UqQltXgaZmoW2gxN5joLHVE6y0qDsdKjMWQikbL_Q8w2Ebvuj6BaF7BxwtnhTn-rxEZWRo1CYJVtPvTkxum9QdruIDLPoN5ZArZxo73054ZGi6pSxke6BzCT8mEQWSuQKvny8s9x8oVO-TbNQJvu9Ah3R8Uwu6N1Q"

    # database:
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    # sqlite:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'todos.sqlite')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://udacity:udacity@db:5432/udasocialbloggingapp'

# configs:
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}