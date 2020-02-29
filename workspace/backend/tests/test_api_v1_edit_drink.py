import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.auth.models import User
from application.models import Drink, DrinkFactory

from base64 import b64encode

class APIV1EditDrinkTestCase(unittest.TestCase):
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

    def get_api_headers(self, email, password):  
        """ api header generation
        """      
        return {            
            'Authorization': 'Basic ' + b64encode(
                (email + ':' + password).encode('utf-8')
            ).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_no_auth(self):
        """  response should have status code 401 and json {"success": False} when authentication is not given
        """
        response = self.client.patch(
            url_for('api_v1.edit_drink',  id = 999),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)

    def test_edit_drink_from_empty_table(self):
        """  response should have status code 404 and json {"success": False, "drinks": drinks} where the given drink doesn't exist
        """
        # remove tables:
        db.drop_all()
        db.create_all()

        # create account:
        manager = User(
            username='manager',
            email='manager@udaspicelatte.com', 
            password='manager'
        )
        db.session.add(manager)
        db.session.commit()

        # generate:
        drink = DrinkFactory()

        # send request:
        response = self.client.patch(
            url_for('api_v1.edit_drink', id = drink.id + 10000), 
            headers=self.get_api_headers(
                email = 'manager@udaspicelatte.com', 
                password = 'manager'
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": drink.title,
                    "recipe": json.loads(
                        drink.recipe
                    )
                }
            )
        )      
        
        # check status code:
        self.assertEqual(response.status_code, 500)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check success:
        self.assertEqual(
            json_response["success"], False
        )

    def test_edit_drink(self):
        """  response should have status code 200 and json {"success": True, "delete": id} where drink an array containing only the updated drink
        """
        # create account:
        manager = User(
            username='manager',
            email='manager@udaspicelatte.com', 
            password='manager'
        )
        db.session.add(manager)
        db.session.commit()

        # generate drink:
        drink = DrinkFactory()
        db.session.add(drink)
        db.session.commit()

        # send request:
        new_title = drink.title + "Updated"
        response = self.client.patch(
            url_for('api_v1.edit_drink', id = drink.id), 
            headers=self.get_api_headers(
                email = 'manager@udaspicelatte.com', 
                password = 'manager'
            ),
            content_type='application/json',
            data = json.dumps(
                {
                    "title": new_title,
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
        # check drink:
        drink = json_response["drinks"][0]
        self.assertEqual(drink["title"], new_title)