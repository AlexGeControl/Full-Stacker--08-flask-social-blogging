import unittest

from flask import current_app

from application import create_app, db

class SetupTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # activate app context:
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create tables:
        db.create_all()

    def tearDown(self):
        # flush transaction:
        db.session.remove()
        # remove all tables:
        db.drop_all()
        # deactivate app context:
        self.app_context.pop()

    def test_app_exists(self):
        """ app should be created
        """
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """ testing config should be used
        """
        self.assertTrue(current_app.config['TESTING'])

    def test_db_connection(self):
        """ db connection specification should be docker-compose default
        """
        self.assertTrue(
            current_app.config['SQLALCHEMY_DATABASE_URI'], 
            'postgresql://udacity:udacity@db:5432/udasocialbloggingapp'
        )