import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Drink, DrinkFactory


class APIV2GetDrinksDetailTestCase(unittest.TestCase):
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

    def test_get_drinks_detail_role_public(self):
        """  response should have status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks with detail
        """
        # generate drinks:
        for _ in range(3):
            # generate:
            drink = DrinkFactory()
            # insert:
            db.session.add(drink)
            db.session.commit()

        # send request:
        response = self.client.get(
            url_for('api_v2.get_drinks_detail'), 
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

    def test_get_drinks_detail_role_barista(self):
        """  response should have status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks with detail
        """
        # generate drinks:
        for _ in range(3):
            # generate:
            drink = DrinkFactory()
            # insert:
            db.session.add(drink)
            db.session.commit()

        # send request:
        response = self.client.get(
            url_for('api_v2.get_drinks_detail'), 
            headers=self.get_api_headers(
                token = current_app.config['AUTH0_ROLE_BARISTA']
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
            len(json_response["drinks"]), 3
        )
        # check recipe details:
        for drink in json_response["drinks"]:
            self.assertTrue("title" in drink)
            self.assertTrue("recipe" in drink)

            for ingredient in drink["recipe"]:
                self.assertTrue("color" in ingredient)
                self.assertTrue("parts" in ingredient)
                self.assertTrue("name" in ingredient)

    def test_get_drinks_detail_from_empty_db_role_manager(self):
        """  response should have status code 500 and json {"success": False} when the drinks table is not created
        """
        # remove tables:
        db.drop_all()

        # send request:
        response = self.client.get(
            url_for('api_v2.get_drinks_detail'), 
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

    def test_get_drinks_detail_from_empty_table_role_manager(self):
        """  response should have status code 200 and json {"success": True, "drinks": drinks} where drinks is an empty list
        """
        # send request:
        response = self.client.get(
            url_for('api_v2.get_drinks_detail'), 
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
        # check status:
        self.assertEqual(
            json_response["success"], True
        )
        # check drinks:
        self.assertEqual(
            len(json_response["drinks"]), 0
        )

    def test_get_drinks_detail_role_manager(self):
        """  response should have status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks with detail
        """
        # generate drinks:
        for _ in range(3):
            # generate:
            drink = DrinkFactory()
            # insert:
            db.session.add(drink)
            db.session.commit()

        # send request:
        response = self.client.get(
            url_for('api_v2.get_drinks_detail'), 
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
            len(json_response["drinks"]), 3
        )
        # check recipe details:
        for drink in json_response["drinks"]:
            self.assertTrue("title" in drink)
            self.assertTrue("recipe" in drink)

            for ingredient in drink["recipe"]:
                self.assertTrue("color" in ingredient)
                self.assertTrue("parts" in ingredient)
                self.assertTrue("name" in ingredient)
