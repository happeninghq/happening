""" Test basic index page. """

from website.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestIndex(TestCase):

    """ Test Index Page. """

    def test_index_no_events(self):
        """ Test it returns when there are no events. """
        response = self.client.get("/")
        self.assertIsNotNone(response.soup.find(id="no-events"))
        self.assertIsNone(response.soup.find(id="next-event"))
        self.assertIsNone(response.soup.find(id="recent-event"))

    def test_latest_event_future(self):
        """ Test it renders the latest event in the future. """
        mommy.make("Event", datetime=datetime.now(pytz.utc) +
                   timedelta(days=20))
        response = self.client.get("/")
        self.assertIsNotNone(response.soup.find(id="next-event"))
        self.assertIsNone(response.soup.find(id="no-events"))
        self.assertIsNone(response.soup.find(id="recent-event"))

    def test_latest_event_past(self):
        """ Test it renders the latest event in the past. """
        mommy.make("Event", datetime=datetime.now(pytz.utc) -
                   timedelta(days=20))
        response = self.client.get("/")
        self.assertIsNotNone(response.soup.find(id="recent-event"))
        self.assertIsNone(response.soup.find(id="no-events"))
        self.assertIsNone(response.soup.find(id="next-event"))
