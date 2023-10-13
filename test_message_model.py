"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py
#
# or FLASK_DEBUG=False python3 -m unittest test_message_model.py


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


class MessageModelTestCase(TestCase):
    def setUp(self):
        Message.query.delete()

        # if messages are normally created in a form, how will we create them here?
        m1 = Message(
            text="This is test message text with the number 1 in it"
        )

        m2 = Message(
            text="Different test message text with the number 2 in it"
        )

        # messages need a user, append messages to user

        db.session.commit()

        self.m1_id = m1.id
        self.m2_id = m2.id


    def tearDown(self):
        db.session.rollback()


    def test_message_model(self):
        ''' testing if the setup is working '''

        m1 = Message.query.get(self.m1_id)

        # m1 is None :(
        # not creating Message instances properly
        self.assertIsInstance(m1, Message)