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
        User.query.delete()

        m_user = User.signup("u5", "u5@email.com", "password", None)
        m_user2 = User.signup("u6", "u6@email.com", "password", None)

        db.session.commit()

        m1 = Message(
            text="This is test message text with the number 1 in it"
        )

        m2 = Message(
            text="Different test message text with the number 2 in it"
        )

        m_user.messages.append(m1)
        m_user2.messages.append(m2)


        db.session.commit()

        self.m1_id = m1.id
        self.m2_id = m2.id

        self.m_user_id = m_user.id
        self.m_user2_id = m_user2.id



    def tearDown(self):
        db.session.rollback()


    def test_message_model(self):
        ''' testing if the setup is working '''

        m1 = Message.query.get(self.m1_id)

        self.assertIsInstance(m1, Message)


    def test_add_message_to_user_messages(self):
        ''' test adding a Message to a User's list of messages '''

        m_user = User.query.get(self.m1_id)

        m3 = Message(
            text='Brand new message'
        )

        m_user.messages.append(m3)

        self.assertIn(m3, m_user.messages)


    def test_remove_message_from_user_messages(self):
        ''' test removing a Message from a User's list of messages'''

        m_user = User.query.get(self.m1_id)

        message = Message.query.get(self.m1_id)

        m_user.messages.remove(message)

        self.assertNotIn(message, m_user.messages)

