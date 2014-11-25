""" Test basic index page. """

from django_bs_test import TestCase
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

    def test_previous_dojos_no_events(self):
        """ Test there are no previous dojos listed. """
        response = self.client.get("/")
        self.assertIsNone(response.soup.find(id="previous-dojos").find("li"))

    def test_previous_dojos(self):
        """ Test is lists previous dojos in the correct order. """
        later_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                 timedelta(days=20))
        response = self.client.get("/")
        self.assertEqual(1, len(
            response.soup.find(id="previous-dojos").findAll("li")))
        earlier_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                   timedelta(days=50))
        response = self.client.get("/")
        lis = response.soup.find(id="previous-dojos").findAll("li")
        self.assertEqual(2, len(lis))
        self.assertEqual(earlier_event.year_heading(), lis[0].find("a").text)
        self.assertEqual(later_event.year_heading(), lis[1].find("a").text)

        # Make a future event which shouldn't appear in the list
        mommy.make("Event", datetime=datetime.now(pytz.utc) +
                   timedelta(days=50))
        response = self.client.get("/")
        self.assertEqual(2, len(
            response.soup.find(id="previous-dojos").findAll("li")))

        # Check that links work correctly
        response = self.client.get(lis[0].find("a")['href'])
        self.assertEqual(earlier_event, response.context['event'])
