"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py
#
# or FLASK_DEBUG=False python3 -m unittest test_user_model.py


import os
from unittest import TestCase

from sqlalchemy.exc import IntegrityError

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


    def test_valid_user_signup(self):
        ''' test success cases for the User signup method '''

        u3 = User.signup("u3", "u3@email.com", "password", None)

        self.assertIsInstance(u3, User)
        self.assertEqual(u3.username, 'u3')
        self.assertEqual(u3.email, 'u3@email.com')
        # check that password not equal password b/c it's hashed now
        self.assertNotEqual(u3.password, 'password')
        # could also do a check that it starts with $2b$ which all bcrypt hashes should start with


    def test_invalid_signup(self):
        ''' test cases that should not result in successful user sign up'''

        with self.assertRaises(IntegrityError):
            User.signup("u1", "u1@email.com", "password", None)

            db.session.commit()



    def test_valid_user_authenticate(self):
        ''' test cases for successful paths re User authenticate method '''

        u1 = User.query.get(self.u1_id)

        self.assertIsInstance(u1.authenticate('u1', 'password'), User)

        authenticated_user = u1.authenticate('u1', 'password')
        self.assertIs(u1, authenticated_user)



    def test_invalid_user_authenticate(self):
        ''' test cases that should not be successful re User authenticate '''

        u1 = User.query.get(self.u1_id)

        self.assertEqual(u1.authenticate('wrong username', 'password'), False)
        self.assertEqual(u1.authenticate('u1', 'wrong password'), False)