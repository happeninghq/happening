"""Test previous events page."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestEvents(TestCase):
    """Test previous events page."""

    def test_previous_events(self):
        """Test that previous events are listed correctly."""
        response = self.client.get("/events/past")
        self.assertEqual(0, len(response.soup.find(id="events-list").findAll(
            class_="event-block")))

        later_event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                 timedelta(days=20))
        response = self.client.get("/events/past")

        self.assertEqual(1, len(response.soup.find(id="events-list").findAll(
            class_="event-block")))

        earlier_event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                   timedelta(days=50))
        response = self.client.get("/events/past")

        blocks = response.soup.find(id="events-list").findAll(
            class_="event-block")

        self.assertEqual(2, len(blocks))
        self.assertEqual(str(later_event), blocks[0].find("a").text)
        self.assertEqual(str(earlier_event), blocks[1].find("a").text)

        # Check that links work correctly
        response = self.client.get(blocks[0].find("a")['href'])
        self.assertEqual(later_event, response.context['event'])

    def test_upcoming_events(self):
        """Test that upcoming events are listed correctly."""
        response = self.client.get("/events/")
        self.assertEqual(0, len(response.soup.find(id="events-list").findAll(
            class_="event-block")))

        later_event = mommy.make("Event", start=datetime.now(pytz.utc) +
                                 timedelta(days=50))
        response = self.client.get("/events/")

        self.assertEqual(1, len(response.soup.find(id="events-list").findAll(
            class_="event-block")))

        earlier_event = mommy.make("Event", start=datetime.now(pytz.utc) +
                                   timedelta(days=20))
        response = self.client.get("/events/")

        blocks = response.soup.find(id="events-list").findAll(
            class_="event-block")

        self.assertEqual(2, len(blocks))
        self.assertEqual(str(later_event), blocks[0].find("a").text)
        self.assertEqual(str(earlier_event), blocks[1].find("a").text)

        # Check that links work correctly
        response = self.client.get(blocks[0].find("a")['href'])
        self.assertEqual(later_event, response.context['event'])
