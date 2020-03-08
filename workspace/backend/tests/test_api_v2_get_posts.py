import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.auth.v2.models import DelegatedUser
from application.models import Post, PostFactory


class APIV2GetPostsTestCase(unittest.TestCase):
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

    def test_get_posts_from_empty_table(self):
        """  response should have status code 200 and en empty list when posts is empty
        """
        # remove tables:
        db.drop_all()
        # create tables:
        db.create_all()

        # send request:
        response = self.client.get(
            '/api/v2/posts/', 
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        posts = json.loads(
            response.get_data(as_text=True)
        )

        # check posts:
        self.assertEqual(
            len(posts), 0
        )

    def test_get_posts(self):
        """  response should have status code 200 and a list of posts
        """
        # remove tables:
        db.drop_all()
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

        # add posts:
        from random import randint
        while Post.query.count() < current_app.config['POSTS_PER_PAGE'] + 1:
            # in case the Faker creates a duplicated post:
            try:
                # random author selection:
                author = DelegatedUser.query.offset(
                    randint(0, user_count - 1)
                ).first()
                # create post:
                post = PostFactory(author_id = author.id)
                db.session.add(post)
                db.session.commit()
            except:
                db.session.rollback()
        db.session.close()
        # get post summary:
        post_count = Post.query.count()

        # send request:
        response = self.client.get(
            '/api/v2/posts/', 
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        posts = json.loads(
            response.get_data(as_text=True)
        )

        # check drinks:
        self.assertEqual(
            len(posts), current_app.config['POSTS_PER_PAGE']
        )
        # check recipe details:
        for post in posts:
            self.assertTrue("id" in post)
            self.assertTrue("title" in post)
            self.assertTrue("author" in post)
            self.assertTrue("timestamp" in post)
