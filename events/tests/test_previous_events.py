""" Test previous events page. """

from website.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestPreviousEvents(TestCase):

    """ Test previous events page. """

    def test_previous_events(self):
        """ Test that previous events are listed correctly. """
        response = self.client.get("/events/previous")
        self.assertIsNone(response.soup.find(id="all-previous-dojos"))

        later_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                 timedelta(days=20))
        response = self.client.get("/events/previous")
        self.assertEqual(1, len(
            response.soup.find(id="all-previous-dojos").findAll(
                "li")))
        earlier_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                   timedelta(days=50))
        response = self.client.get("/events/previous")
        lis = response.soup.find(id="all-previous-dojos").findAll(
            "li")
        self.assertEqual(2, len(lis))
        self.assertEqual(later_event.year_heading(), lis[0].find("a").text)
        self.assertEqual(earlier_event.year_heading(), lis[1].find("a").text)

        # Make a future event which shouldn't appear in the list
        mommy.make("Event", datetime=datetime.now(pytz.utc) +
                   timedelta(days=50))
        response = self.client.get("/events/previous")
        self.assertEqual(2, len(
            response.soup.find(id="all-previous-dojos").findAll(
                "li")))

        # Check that links work correctly
        response = self.client.get(lis[0].find("a")['href'])
        self.assertEqual(later_event, response.context['event'])

        # Check that it only shows five
        for i in range(10):
            mommy.make("Event", datetime=datetime.now(pytz.utc) -
                       timedelta(days=i * 13))

        response = self.client.get("/events/previous")
        self.assertEqual(12, len(
            response.soup.find(id="all-previous-dojos").findAll(
                "li")))
