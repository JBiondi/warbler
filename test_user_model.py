"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py
#
# or FLASK_DEBUG=False python3 -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follow

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        ''' provided test that tests the user setup '''
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)


    def test_user_is_following(self):
        ''' test cases for the is_following method '''

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u2.followers.append(u1)

        self.assertEqual(u1.is_following(u2), True)

        u2.followers.remove(u1)
        self.assertEqual(u1.is_following(u2), False)


    def test_user_is_followed_by(self):
        ''' test cases for the User is_followed_by method '''

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.followers.append(u2)
        self.assertEqual(u1.is_followed_by(u2), True)

        u1.followers.remove(u2)
        self.assertEqual(u1.is_followed_by(u2), False)


    def test_user_signup(self):
        ''' test cases for the User signup method '''

        u3 = User.signup("u3", "u3@email.com", "password", None)

        self.assertIsInstance(u3, User)
        self.assertEqual(u3.username, 'u3')
        self.assertEqual(u3.email, 'u3@email.com')
        # could check that password not equal password b/c it's hashed now $2b$
        self.assertNotEqual(u3.password, 'password')

        # u4 = User.signup("u3", "u4@gamil.com", "password", None)
        # causes error, how to test for that without crashing app?

    # def test_invalid_signup(self):
    # # Assert that user signup raises an integrity error when we make a user
    # # with the same username

    #     with self.assertRaises(IntegrityError):
    #         User.signup("u1", "u1@email.com", "password", None)
    #         db.session.commit()

        # all_users = User.query.all()
        # self.assertNotIn(u4, all_users)


    def test_user_authenticate(self):
        ''' test cases for the User authenticate method '''

        u1 = User.query.get(self.u1_id)

        # how to test if it's the correct user though?
        self.assertIsInstance(u1.authenticate('u1', 'password'), User)
        # does authenticated_user = u1.authenticate

        # TODO: break into separate tests
        self.assertEqual(u1.authenticate('wrong username', 'password'), False)
        self.assertEqual(u1.authenticate('u1', 'wrong password'), False)
