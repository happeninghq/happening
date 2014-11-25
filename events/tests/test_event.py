""" Test event model. """

from unittest import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestIndex(TestCase):

    """ Test event model. """

    def test_is_future(self):
        """ Test that is_future works. """
        past_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                timedelta(days=20))
        self.assertFalse(past_event.is_future())
        future_event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                                  timedelta(days=20))
        self.assertTrue(future_event.is_future())
