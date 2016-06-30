"""Test emails."""

from happening.tests import TestCase
from django.core import mail
from emails.models import Email


class TestEmails(TestCase):

    """Test emails."""

    # def setUp(self):
    #     super(TestEmails, self).setUp()

    def test_send_email(self):
        """Test that we can send an email."""
        Email(to="test@happeninghq.com", subject="s", content="c").save()
        self.assertEquals(len(mail.outbox), 1)
