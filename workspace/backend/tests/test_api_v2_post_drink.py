import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Drink, DrinkFactory


class APIV2PostDrinksTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # activate app context:
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create tables:
        db.create_all()
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

    def test_post_drink_role_public(self):
        """  response should have status code 403 and json {"success": False} using role public
        """        
        # generate drink:
        drink = DrinkFactory()

        # send request:
        response = self.client.post(
            url_for('api_v2.create_drink'),
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_PUBLIC']
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": drink.title + 'Exclusive',
                    "recipe": json.loads(
                        drink.recipe
                    )
                }
            )
        )

        # check status code:
        self.assertEqual(response.status_code, 401)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )

        # check success:
        self.assertEqual(
            json_response["success"], False
        )

    def test_post_drink_role_barista(self):
        """  response should have status code 403 and json {"success": False} using role barista
        """        
        # generate drink:
        drink = DrinkFactory()

        # send request:
        response = self.client.post(
            url_for('api_v2.create_drink'),
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_BARISTA']
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": drink.title + 'Exclusive',
                    "recipe": json.loads(
                        drink.recipe
                    )
                }
            )
        )

        # check status code:
        self.assertEqual(response.status_code, 403)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )

        # check success:
        self.assertEqual(
            json_response["success"], False
        )

    def test_post_drink_role_manager(self):
        """  response should have status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        """        
        # generate drink:
        drink = DrinkFactory()

        # send request:
        response = self.client.post(
            url_for('api_v2.create_drink'),
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_MANAGER']
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": drink.title + 'Exclusive',
                    "recipe": json.loads(
                        drink.recipe
                    )
                }
            )
        )

        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )

        # check success:
        self.assertEqual(
            json_response["success"], True
        )
        self.assertEqual(
            len(json_response["drinks"]), 1
        )

        # check drink
        drink = json_response["drinks"][0]
        self.assertTrue("title" in drink)
        self.assertTrue("recipe" in drink)
        for ingredient in drink["recipe"]:
            self.assertTrue("color" in ingredient)
            self.assertTrue("parts" in ingredient)
            self.assertTrue("name" in ingredient)

    def test_post_duplicated_drink_role_manager(self):
        """  response should have status code 500 and json {"success": False} where drink has a duplicated name
        """        
        # generate drink:
        drink = DrinkFactory()

        # send request:
        response = self.client.post(
            url_for('api_v2.create_drink'),
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_MANAGER']
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": drink.title + 'Exclusive',
                    "recipe": json.loads(
                        drink.recipe
                    )
                }
            )
        )

        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )

        # check success:
        self.assertEqual(
            json_response["success"], True
        )
        self.assertEqual(
            len(json_response["drinks"]), 1
        )

        # check drink
        drink = json_response["drinks"][0]
        self.assertTrue("title" in drink)
        self.assertTrue("recipe" in drink)
        for ingredient in drink["recipe"]:
            self.assertTrue("color" in ingredient)
            self.assertTrue("parts" in ingredient)
            self.assertTrue("name" in ingredient)

        # send request:
        response = self.client.post(
            url_for('api_v2.create_drink'),
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_MANAGER']
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": drink["title"],
                    "recipe": drink["recipe"]
                }
            )
        )

        # check status code:
        self.assertEqual(response.status_code, 500)
