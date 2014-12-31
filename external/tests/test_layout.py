""" Test basic layout. """

from website.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestLayout(TestCase):

    """ Test basic layout. """

    def test_shows_login_link(self):
        """ Test it shows a login link if the user is logged out. """
        response = self.client.get("/")
        self.assertIsNotNone(
            response.soup.find("a", {"href": "/accounts/login/"}))
        self.assertIsNone(
            response.soup.find("a", {"href": "/accounts/logout/"}))

    def test_shows_logged_in_links(self):
        """ Test it has appropriate links for logged in users. """
        user = mommy.make("auth.User")
        user.set_password("password")
        user.save()

        self.client.login(username=user.username, password="password")

        response = self.client.get("/")
        self.assertIsNone(
            response.soup.find("a", {"href": "/accounts/login/"}))
        self.assertIsNotNone(
            response.soup.find("a", {"href": "/accounts/logout/"}))

    def test_previous_dojos_no_events(self):
        """ Test there are no previous dojos listed. """
        response = self.client.get("/")
        self.assertIsNone(response.soup.find(id="previous-dojos").find(
            "li", {"class": "dojo"}))

    def test_previous_dojos(self):
        """ Test is lists previous dojos in the correct order. """
        later_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                 timedelta(days=20))
        response = self.client.get("/")
        self.assertEqual(1, len(
            response.soup.find(id="previous-dojos").findAll(
                "li", {"class": "dojo"})))
        earlier_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                   timedelta(days=50))
        response = self.client.get("/")
        lis = response.soup.find(id="previous-dojos").findAll(
            "li", {"class": "dojo"})
        self.assertEqual(2, len(lis))
        self.assertEqual(later_event.year_heading(), lis[0].find("a").text)
        self.assertEqual(earlier_event.year_heading(), lis[1].find("a").text)

        # Make a future event which shouldn't appear in the list
        mommy.make("Event", datetime=datetime.now(pytz.utc) +
                   timedelta(days=50))
        response = self.client.get("/")
        self.assertEqual(2, len(
            response.soup.find(id="previous-dojos").findAll(
                "li", {"class": "dojo"})))

        # Check that links work correctly
        response = self.client.get(lis[0].find("a")['href'])
        self.assertEqual(later_event, response.context['event'])

        # Check that it only shows five
        for i in range(10):
            mommy.make("Event", datetime=datetime.now(pytz.utc) -
                       timedelta(days=i * 13))

        response = self.client.get("/")
        self.assertEqual(5, len(
            response.soup.find(id="previous-dojos").findAll(
                "li", {"class": "dojo"})))