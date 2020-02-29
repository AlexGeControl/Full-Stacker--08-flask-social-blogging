import unittest

from application.auth.models import User

class ModelUserTestCase(unittest.TestCase):
    def test_password_setter(self):
        """ password hash should be set when new password is given
        """
        user = User(password = 'goose')

        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        """ password should not be readable attribute
        """
        user = User(password = 'goose')

        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        """ password should be verified using password hash only
        """
        user = User(password = 'goose')

        # pass:
        self.assertTrue(user.verify_password('goose'))
        # failed:
        self.assertFalse(user.verify_password('dog'))

    def test_password_salts_are_random(self):
        """ salt should be added to password hash
        """
        user_one = User(password='goose')
        user_another = User(password='goose')

        self.assertTrue(user_one.password_hash != user_another.password_hash)