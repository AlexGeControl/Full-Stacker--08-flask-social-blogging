import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Drink, DrinkFactory


class APIV2DeleteDrinksTestCase(unittest.TestCase):
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

    def test_delete_drink_role_public(self):
        """  response should have status code 200 and json {"success": False} with role public
        """
        # generate drinks:
        for _ in range(3):
            # generate:
            drink = DrinkFactory()
            # insert:
            db.session.add(drink)
            db.session.commit()

        # send request:
        response = self.client.delete(
            url_for('api_v2.delete_drink', id = drink.id), 
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_PUBLIC']
            ),
            content_type='application/json'
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

    def test_delete_drink_role_barista(self):
        """  response should have status code 200 and json {"success": False} with role barista
        """
        # generate drinks:
        for _ in range(3):
            # generate:
            drink = DrinkFactory()
            # insert:
            db.session.add(drink)
            db.session.commit()

        # send request:
        response = self.client.delete(
            url_for('api_v2.delete_drink', id = drink.id), 
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_BARISTA']
            ),
            content_type='application/json'
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

    def test_delete_drink_from_empty_db_role_manager(self):
        """  response should have status code 500 and json {"success": False} when the drinks table is not created
        """
        # remove tables:
        db.drop_all()

        # send request:
        response = self.client.delete(
            url_for('api_v2.delete_drink', id = 1), 
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_MANAGER']
            ),
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 500)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check status:
        self.assertEqual(
            json_response["success"], False
        )

    def test_delete_drink_from_empty_table_role_manager(self):
        """  response should have status code 404 and json {"success": False, "drinks": drinks} where the given drink doesn't exist
        """
        # generate:
        drink = DrinkFactory()
        # insert:
        db.session.add(drink)
        db.session.commit()

        # send request:
        response = self.client.delete(
            url_for('api_v2.delete_drink', id = drink.id + 1), 
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_MANAGER']
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

    def test_delete_drink_role_manager(self):
        """  response should have status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        """
        # generate drinks:
        for _ in range(3):
            # generate:
            drink = DrinkFactory()
            # insert:
            db.session.add(drink)
            db.session.commit()

        # send request:
        response = self.client.delete(
            url_for('api_v2.delete_drink', id = drink.id), 
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_MANAGER']
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