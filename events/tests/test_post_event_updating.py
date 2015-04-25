"""Test event view."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from django.conf import settings


class TestPostEventUpdating(TestCase):

    """Test updating details after an event."""

    def setUp(self):
        """Set up a common user."""
        self.user = mommy.make(settings.AUTH_USER_MODEL,
                               email="test@example.com")
        self.user.set_password("password")
        self.user.save()

    def test_future_event(self):
        """Test that update details doesn't appear for future event."""
        future_event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                                  timedelta(days=20), available_tickets=30)
        mommy.make("Ticket", event=future_event, user=self.user, number=1)
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/events/%s" % future_event.id)
        self.assertEquals(response.status_code, 200)
        widget = response.soup.find("div", {"class": "update-group"})
        self.assertIsNone(widget)
        widget = response.soup.find("div", {"class": "set-group"})
        self.assertIsNone(widget)

    # def test_set_group(self):
    #     """Test that a member can set the group they were part of."""
    #     event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
    #                        timedelta(days=20), available_tickets=30)
    #     mommy.make("Ticket", event=event, user=self.user, number=1)
    #     self.client.login(username=self.user.username, password="password")
    #     response = self.client.get("/events/%s" % event.id)

    #     widget = response.soup.find("div", {"class": "update-group"})
    #     self.assertIsNone(widget)
    #     widget = response.soup.find("div", {"class": "set-group"})
    #     self.assertIsNotNone(widget)

    #     response = self.client.post("/events/%s/set_group" % event.id,
    #                                 {"group_number": "1"}, follow=True)
    #     self.assertTrue("/events/%s" % event.id in
    #                     response.redirect_chain[0][0])
    #     widget = response.soup.find("div", {"class": "set-group"})
    #     self.assertIsNone(widget)
    #     widget = response.soup.find("div", {"class": "update-group"})
    #     self.assertIsNotNone(widget)

    # def test_update_group(self):
    #     """Test updating group."""
    #     event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
    #                        timedelta(days=20), available_tickets=30)
    #     mommy.make("Ticket", event=event, user=self.user, number=1)
    #     self.client.login(username=self.user.username, password="password")
    #     response = self.client.post("/events/%s/set_group" % event.id,
    #                                 {"group_number": "1"}, follow=True)
    #     response = self.client.get("/events/%s" % event.id)
    #     self.assertIsNone(response.soup.find(id="event-solutions"))
    #     widget = response.soup.find("div", {"class": "update-group"})
    #     self.assertIsNotNone(widget)
    #     response = self.client.post("/events/%s/group" % event.id,
    #                                 {"description": "DESCRIPTION",
    #                                  "github_url": "http://google.com"},
    #                                 follow=True)
    #     self.assertTrue("/events/%s" % event.id in
    #                     response.redirect_chain[0][0])
    #     widget = response.soup.find("div", {"class": "update-group"})
    #     self.assertIsNone(widget)
    #     solutions = response.soup.find(id="event-solutions")
    #     self.assertIsNotNone(solutions)
    #     self.assertEqual("Group 1", solutions.find("a").text)
    #     self.assertEqual("http://google.com/", solutions.find("a")['href'])
    #     self.assertEqual("DESCRIPTION", solutions.find("td").text)

    # def test_group_already_updated(self):
    #     """Test that we can't update a group a second time."""
    #     event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
    #                        timedelta(days=20), available_tickets=30)
    #     mommy.make("Ticket", event=event, user=self.user, number=1)
    #     self.client.login(username=self.user.username, password="password")
    #     response = self.client.post("/events/%s/set_group" % event.id,
    #                                 {"group_number": "1"}, follow=True)
    #     response = self.client.get("/events/%s" % event.id)
    #     self.assertIsNone(response.soup.find(id="event-solutions"))
    #     widget = response.soup.find("div", {"class": "update-group"})
    #     self.assertIsNotNone(widget)
    #     response = self.client.post("/events/%s/group" % event.id,
    #                                 {"description": "DESCRIPTION",
    #                                  "github_url": "http://google.com"},
    #                                 follow=True)
    #     user = mommy.make(settings.AUTH_USER_MODEL, email="test@example.com")
    #     user.set_password("password")
    #     user.save()
    #     self.client.login(username=user.username, password="password")
    #     response = self.client.get("/events/%s" % event.id)
    #     widget = response.soup.find("div", {"class": "update-group"})
    #     self.assertIsNone(widget)

    # def test_did_not_attend(self):
    #     """Test that marking did not attent does not allow update group."""
    #     event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
    #                        timedelta(days=20), available_tickets=30)
    #     mommy.make("Ticket", event=event, user=self.user, number=1)
    #     self.client.login(username=self.user.username, password="password")
    #     response = self.client.post("/events/%s/set_group" % event.id,
    #                                 {"group_number": "0"}, follow=True)
    #     response = self.client.get("/events/%s" % event.id)
    #     self.assertIsNone(response.soup.find(id="event-solutions"))
    #     widget = response.soup.find("div", {"class": "update-group"})
    #     self.assertIsNone(widget)
