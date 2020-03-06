import json
from jose import jwt

import requests
from urllib.request import urlopen
import urllib.parse

from flask import current_app
from flask import jsonify
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from config import config

class AuthError(Exception):
    """ exception for Auth0 JWT verification
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

#  Auth0 service
#  ----------------------------------------------------------------
class Provider:
    def __init__(self, domain, token, algorithms):
        self.domain = domain
        self.token = token
        self.algorithms = algorithms

    @property
    def jwks_url(self):
        return f'{self.domain}.well-known/jwks.json'

    @property
    def headers(self):
        """ authorization header
        """
        return {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get(self, url, params={}):
        """ GET
        """
        return requests.get(
            url, 
            headers=self.headers, 
            params=params
        )

    def post(self, url, data):
        """ POST
        """
        return requests.post(
            url, 
            headers=self.headers, 
            json=data
        )

    def delete(self, url, params={}):
        """ DELETE
        """
        return requests.delete(
            url, 
            headers=self.headers, 
            params=params
        )

    def decode_token(self, audience, token):
        """ verify and decode JWT for Auth0
        """
        # load public keys:
        jwks = json.loads(
            urlopen(
                self.jwks_url
            )
        )

        # extract JWT header:
        unverified_header = jwt.get_unverified_header(token)
        if 'kid' not in unverified_header:
            raise AuthError(
                {
                    'code': 'invalid_header',
                    'description': 'Authorization malformed.'
                }, 
                401
            )

        # select the public key declared in JWT:
        rsa_key = None
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }

        # if matching key is selected:
        if not (rsa_key is None):
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.algorithms,
                    audience=audience,
                    issuer=self.domain
                )

                return payload
            # if token has expired:
            except jwt.ExpiredSignatureError:
                raise AuthError(
                    {
                        'code': 'token_expired',
                        'description': 'Token expired.'
                    }, 
                    401
                )
            except jwt.JWTClaimsError:
                raise AuthError(
                    {
                        'code': 'invalid_claims',
                        'description': 'Incorrect claims. Please, check the audience and issuer.'
                    }, 
                    401
                )
            except Exception:
                raise AuthError(
                    {
                        'code': 'invalid_header',
                        'description': 'Unable to parse authentication token.'
                    }, 
                    400
                )
        # if no matching key is found:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 
            400
        )

#  user profile services
#  ----------------------------------------------------------------
class UserByEmail(Resource):
    # backend:
    provider = Provider( 
        domain = config['default'].AUTH0_DOMAIN_URL, 
        token = config['default'].AUTH0_MANAGEMENT_TOKEN,
        algorithms = config['default'].AUTH0_ALGORITHMS,
    )
    # endpoint:
    url = f'{config["default"].AUTH0_DOMAIN_URL}api/v2/users-by-email'

    def get(self, email):
        """ get user by email
        """
        # query params:
        params = {
            'email': email
        }

        # user info:
        response = self.provider.get(self.url, params)

        return response.json()

#  account management services
#  ----------------------------------------------------------------
class Users(Resource):
    # backend:
    provider = Provider( 
        domain = config['default'].AUTH0_DOMAIN_URL, 
        token = config['default'].AUTH0_MANAGEMENT_TOKEN,
        algorithms = config['default'].AUTH0_ALGORITHMS,
    )
    # endpoint:
    url = f'{config["default"].AUTH0_DOMAIN_URL}api/v2/users'

    def get(self):
        """ list users
        """
        # users:
        response = self.provider.get(self.url)

        return response.json()

    def post(self, email, password):
        """ create a user
        """
        # data:
        data = {
            'email': email,
            'password': password,
            'connection': config['default'].AUTH0_DB_CONNECTION
        }

        # new user info:
        response = self.provider.post(self.url, data)

        return response.json()

    def delete(self, id):
        """ delete a user
        """
        # status info:
        response = self.provider.delete(
            f'{url}/{id}'
        )
        return response.json()