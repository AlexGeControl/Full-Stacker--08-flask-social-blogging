import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.auth.v2.models import DelegatedUser
from application.models import Post, PostFactory


class APIV2DeletePostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # activate app context:
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create tables:
        db.create_all()

        # sycn users from backend:
        from application.auth.v2.services import Users
        service_user_management = Users()
        users = service_user_management.get()

        # add users:
        success = False
        try:
            for user in users:
                # init user:
                _, id = user['user_id'].split('|')
                user = DelegatedUser(
                    id = id,
                    email = user['email'],
                    nickname = user['nickname']
                )
                # add to transaction:
                db.session.add(user)
            db.session.commit()
            success = True
        except:
            db.session.rollback()
            success=False
        finally:
            db.session.close()
        # get user summary:
        user_count = DelegatedUser.query.count()

        # create client:
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        # flush transaction:
        db.session.remove()
        # remove all tables:
        db.drop_all()
        # deactivate app context:
        self.app_context.pop()

    def get_api_headers(self, token):  
        """ api header generation
        """      
        return {            
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_delete_post_role_none(self):
        """  response should have status code 401 when no access token is provided
        """
        # send request:
        response = self.client.post(
            '/api/v2/posts/',
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_USER']
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": "Uda Social Blogging API Testing",
                    "contents": "Will be finished by the end of today."
                }
            )
        )

        # check status code:
        self.assertEqual(response.status_code, 201)

        # parse json response:
        post = json.loads(
            response.get_data(as_text=True)
        )

        # send request:
        response = self.client.delete(
            f'/api/v2/posts/{post["id"]}', 
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_NONE']
            ),
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 401)

    def test_delete_post_role_user(self):
        """  response should have status code 401 using role user
        """
        # send request:
        response = self.client.post(
            '/api/v2/posts/',
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_USER']
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": "Uda Social Blogging API Testing",
                    "contents": "Will be finished by the end of today."
                }
            )
        )

        # check status code:
        self.assertEqual(response.status_code, 201)

        # parse json response:
        post = json.loads(
            response.get_data(as_text=True)
        )
        
        # send request:
        response = self.client.delete(
            f'/api/v2/posts/{post["id"]}', 
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_USER']
            ),
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 403)

    def test_delete_post_role_admin(self):
        """  response should have status code 204 using role admin
        """
        # send request:
        response = self.client.post(
            '/api/v2/posts/',
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_USER']
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": "Uda Social Blogging API Testing",
                    "contents": "Will be finished by the end of today."
                }
            )
        )

        # check status code:
        self.assertEqual(response.status_code, 201)

        # parse json response:
        post = json.loads(
            response.get_data(as_text=True)
        )
        
        # send request:
        response = self.client.delete(
            f'/api/v2/posts/{post["id"]}', 
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_ADMIN']
            ),
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 204)