"""Test event view."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from django.conf import settings


class TestPostEventUpdating(TestCase):
    """Test updating details after an event."""

    def setUp(self):
        """Set up a common user."""
        super(TestPostEventUpdating, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL,
                               email="test@example.com")
        self.user.set_password("password")
        self.user.save()

    def test_future_event(self):
        """Test that update details doesn't appear for future event."""
        future_event = mommy.make("Event", start=datetime.now(pytz.utc) +
                                  timedelta(days=20))
        mommy.make("Ticket", event=future_event, user=self.user)
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/events/%s" % future_event.id)
        self.assertEquals(response.status_code, 200)
        widget = response.soup.find("div", {"class": "update-group"})
        self.assertIsNone(widget)
        widget = response.soup.find("div", {"class": "set-group"})
        self.assertIsNone(widget)
