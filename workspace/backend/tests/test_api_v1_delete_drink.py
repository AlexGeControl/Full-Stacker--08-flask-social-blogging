import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.auth.models import User
from application.models import Drink, DrinkFactory

from base64 import b64encode

class APIV1DeleteDrinksTestCase(unittest.TestCase):
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
        response = self.client.delete(
            url_for('api_v1.delete_drink', id = 999),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_drink_from_empty_table(self):
        """  response should have status code 404 and json {"success": False, "drinks": drinks} where the given drink doesn't exist
        """
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
        # insert:
        db.session.add(drink)
        db.session.commit()

        # send request:
        response = self.client.delete(
            url_for('api_v1.delete_drink', id = drink.id + 1), 
            headers=self.get_api_headers(
                email = 'manager@udaspicelatte.com', 
                password = 'manager'
            ),
            content_type='application/json'
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

    def test_delete_drink(self):
        """  response should have status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        """
        # create account:
        manager = User(
            username='manager',
            email='manager@udaspicelatte.com', 
            password='manager'
        )
        db.session.add(manager)
        db.session.commit()

        # generate drinks:
        for _ in range(3):
            # generate:
            drink = DrinkFactory()
            # insert:
            db.session.add(drink)
        db.session.commit()

        # send request:
        response = self.client.delete(
            url_for('api_v1.delete_drink', id = drink.id), 
            headers=self.get_api_headers(
                email = 'manager@udaspicelatte.com', 
                password = 'manager'
            ),
            content_type='application/json'
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
        # check drinks:
        self.assertEqual(
            json_response["delete"], drink.id
        )

        # check reamaing records:
        self.assertEqual(
            Drink.query.count(), 2
        )