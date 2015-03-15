"""Test event manager."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from events.models import Event


class TestEventManager(TestCase):

    """Test event manager."""

    def test_latest_event_finds_next_future(self):
        """Test that latest_event finds the next future event."""
        next_event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                                timedelta(days=5))
        mommy.make("Event", datetime=datetime.now(pytz.utc) +
                   timedelta(days=20))
        mommy.make("Event", datetime=datetime.now(pytz.utc) -
                   timedelta(days=5))
        self.assertEqual(next_event, Event.objects.latest_event())

    def test_latest_event_finds_previous_event(self):
        """Test that latest_event finds the next future event."""
        last_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                timedelta(days=5))
        mommy.make("Event", datetime=datetime.now(pytz.utc) -
                   timedelta(days=20))
        self.assertEqual(last_event, Event.objects.latest_event())
