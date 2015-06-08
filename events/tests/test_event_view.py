"""Test event view."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestEventView(TestCase):

    """Test Event View."""

    def test_nonexisting_event(self):
        """Test view for event which doesn't exist."""
        response = self.client.get("/events/1")
        self.assertEquals(response.status_code, 404)

    def test_future_event(self):
        """Test view for an event in the future."""
        future_event = mommy.make("Event", start=datetime.now(pytz.utc) +
                                  timedelta(days=20), available_tickets=30)
        response = self.client.get("/events/%s" % future_event.id)
        self.assertEquals(response.status_code, 200)
        widget = response.soup.find("div", {"class": "ticket-purchase"})
        self.assertIsNotNone(widget)
        tickets = widget.find("td", {"class": "remaining-tickets"}).text
        self.assertEqual("30 Tickets", tickets.strip())

    def test_past_event(self):
        """Test view for an event in the past."""
        empty_event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                 timedelta(days=20))
        empty_response = self.client.get("/events/%s" % empty_event.id)
        self.assertEquals(empty_response.status_code, 200)

        # Check heading
        self.assertEquals(str(empty_event),
                          empty_response.soup.find("h2").text)
