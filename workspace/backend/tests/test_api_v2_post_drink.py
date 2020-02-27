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

    def test_post_drink(self):
        """  response should have status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        """        
        # generate drink:
        drink = DrinkFactory()

        # send request:
        response = self.client.post(
            url_for('api_v2.create_drink'),
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

    def test_post_drink(self):
        """  response should have status code 500 and json {"success": False} where drink has a duplicated name
        """        
        # generate drink:
        drink = DrinkFactory()

        # send request:
        response = self.client.post(
            url_for('api_v2.create_drink'),
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
