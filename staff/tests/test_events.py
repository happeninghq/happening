""" Test administrating events. """

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from uuid import uuid4
from django.core import mail
from django.conf import settings


class TestEvents(TestCase):

    """ Test administrating events. """

    def setUp(self):
        """ Set up a user. """
        self.user = mommy.make(settings.AUTH_USER_MODEL, is_staff=True)
        self.user.set_password("password")
        self.user.save()

        self.event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                                timedelta(days=2), available_tickets=30)

    def test_send_email(self):
        """ Test that administrators can send emails to attending members. """
        test_subject = uuid4().hex
        test_content = uuid4().hex
        # With a single attendee
        mommy.make("Ticket", event=self.event, number=1)
        self.client.login(username=self.user.username, password="password")

        self.client.post("/staff/events/%s/email" % self.event.id, {
            "subject": test_subject,
            "content": test_content
            })

        self.assertEquals(1, len(mail.outbox))
        self.assertEquals(test_subject, mail.outbox[0].subject)
        self.assertTrue(test_content in mail.outbox[0].body)
        mail.outbox = []

        # With two attendees
        mommy.make("Ticket", event=self.event, number=1)
        self.client.post("/staff/events/%s/email" % self.event.id, {
            "subject": test_subject,
            "content": test_content
            })
        self.assertEquals(2, len(mail.outbox))
