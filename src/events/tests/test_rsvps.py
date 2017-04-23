"""Test ticket purchasing."""

from happening.tests import TestCase
from model_mommy import mommy
from events.models import Event
from datetime import datetime, timedelta
import pytz
from django.conf import settings


class TestRSVP(TestCase):

    """Test RSVPing."""

    def setUp(self):
        """Set up a common user and event."""
        super(TestRSVP, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL,
                               email="test@example.com")
        self.user.set_password("password")
        self.user.save()

        self.event = mommy.make(
            "Event", start=datetime.now(pytz.utc) +
            timedelta(days=20),
            ticketing_type=Event.TicketingChoices.rsvp)

        self.client.login(username=self.user.username, password="password")

    def test_rsvp(self):
        """Test that we can rsvp to an event."""
        self.assertEqual(0, len(self.event.attending_users()))

        response = self.client.post(
            "/events/%s/rsvp/going" % self.event.pk,
            follow=True)
        self.assertTrue(
            "events/%s/rsvp/going/confirm" % self.event.pk in
            response.redirect_chain[0][0])

        self.assertEqual(1, len(self.event.attending_users()))

        response = self.client.post(
            "/events/%s/rsvp/not_going" % self.event.pk,
            follow=True)
        self.assertTrue(
            "events/%s" % self.event.pk in
            response.redirect_chain[0][0])

        self.assertEqual(0, len(self.event.attending_users()))
