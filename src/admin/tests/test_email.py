"""Test sending emails."""

from happening.tests import TestCase
from model_mommy import mommy
from uuid import uuid4
from django.core import mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class TestEmail(TestCase):

    """Test sending emails."""

    def setUp(self):
        """Set up a user."""
        super(TestEmail, self).setUp()
        self.user = self.create_admin()

    def test_send_email(self):
        """Test that administrators can send emails to all members."""
        test_subject = uuid4().hex
        test_content = uuid4().hex
        self.client.login(username=self.user.username, password="password")

        # With a single attendee
        start_sending = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        stop_sending = (
            timezone.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.client.post("/admin/create_email", {
            "to": "a@b.com",
            "subject": test_subject,
            "content": test_content,
            "sending_range": start_sending + "---" + stop_sending
            })

        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(test_subject, mail.outbox[0].subject)
        self.assertTrue(test_content in mail.outbox[0].body)
        mail.outbox = []

        # With two members
        mommy.make(settings.AUTH_USER_MODEL)
        start_sending = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        stop_sending = (
            timezone.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.client.post("/admin/create_email", {
            "to": "a@b.com,b@c.com",
            "subject": test_subject,
            "content": test_content,
            "sending_range": start_sending + "---" + stop_sending
            })
        self.assertEqual(2, len(mail.outbox))
