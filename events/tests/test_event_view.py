""" Test event view. """

from django_bs_test import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestEventView(TestCase):

    """ Test Event View. """

    def test_nonexisting_event(self):
        """ Test view for event which doesn't exist. """
        response = self.client.get("/events/1")
        self.assertEquals(response.status_code, 404)

    def test_future_event(self):
        """ Test view for an event in the future. """
        mommy.make("Event", datetime=datetime.now(pytz.utc) +
                   timedelta(days=20), id=1)
        response = self.client.get("/events/1")
        self.assertEquals(response.status_code, 404)
