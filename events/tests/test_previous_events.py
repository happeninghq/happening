"""Test previous events page."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestPreviousEvents(TestCase):

    """Test previous events page."""

    def test_previous_events(self):
        """Test that previous events are listed correctly."""
        response = self.client.get("/events/")
        self.assertEqual(
            0, len(response.soup.find(id="all-events").findAll("li")))

        later_event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                 timedelta(days=20))
        response = self.client.get("/events/")
        self.assertEqual(1, len(
            response.soup.find(id="all-events").findAll(
                "li")))
        earlier_event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                   timedelta(days=50))
        response = self.client.get("/events/")
        lis = response.soup.find(id="all-events").findAll(
            "li")
        self.assertEqual(2, len(lis))
        self.assertEqual(str(later_event), lis[0].find("a").text)
        self.assertEqual(str(earlier_event), lis[1].find("a").text)

        # Check that links work correctly
        response = self.client.get(lis[0].find("a")['href'])
        self.assertEqual(later_event, response.context['event'])

        # Check that it only shows five
        for i in range(10):
            mommy.make("Event", start=datetime.now(pytz.utc) -
                       timedelta(days=i * 13))

        response = self.client.get("/events/")
        self.assertEqual(12, len(
            response.soup.find(id="all-events").findAll(
                "li")))
