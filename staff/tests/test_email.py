""" Test sending emails. """

from website.tests import TestCase
from model_mommy import mommy
from uuid import uuid4
from django.core import mail


class TestEmail(TestCase):

    """ Test sending emails. """

    def setUp(self):
        """ Set up a user. """
        self.user = mommy.make("auth.User", is_staff=True)
        self.user.set_password("password")
        self.user.save()

    def test_send_email(self):
        """ Test that administrators can send emails to all members. """
        test_subject = uuid4().hex
        test_content = uuid4().hex
        self.client.login(username=self.user.username, password="password")

        # With a single attendee
        self.client.post("/staff/send_email", {
            "subject": test_subject,
            "content": test_content
            })

        self.assertEquals(1, len(mail.outbox))
        self.assertEquals(test_subject, mail.outbox[0].subject)
        self.assertTrue(test_content in mail.outbox[0].body)
        mail.outbox = []

        # With two members
        mommy.make("auth.User")
        self.client.post("/staff/send_email", {
            "subject": test_subject,
            "content": test_content
            })
        self.assertEquals(2, len(mail.outbox))
