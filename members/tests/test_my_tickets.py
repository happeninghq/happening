"""Test my tickets."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from events.models import Ticket
from django.conf import settings


class TestMyTickets(TestCase):

    """Test my tickets."""

    def setUp(self):
        """Set up a user with some tickets."""
        self.user = mommy.make(settings.AUTH_USER_MODEL)
        self.user.set_password("password")
        self.user.save()

        self.past_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                     timedelta(days=20))
        self.future_event = mommy.make("Event",
                                       datetime=datetime.now(pytz.utc) +
                                       timedelta(days=20))

        self.ticket1 = mommy.make("Ticket", event=self.past_event,
                                  user=self.user, number=1)
        self.ticket2 = mommy.make("Ticket", event=self.future_event,
                                  user=self.user, number=5)

    def test_my_tickets_requires_login(self):
        """Test you need to be logged in to view my tickets."""
        response = self.client.get("/member/tickets", follow=True)
        self.assertTrue("accounts/login" in response.redirect_chain[0][0])

    def test_past_event(self):
        """Test that we can't edit or cancel tickets past the deadline."""
        self.client.login(username=self.user.username, password="password")

        # First check links aren't visible on my tickets
        response = self.client.get("/member/tickets")
        past_ticket = response.soup.findAll("div", {"class": "ticket"})[0]
        self.assertIsNone(past_ticket.find("a", {"class": "button"}))

        # Then check we can't hit the edit or cancel links
        response = self.client.get("/member/tickets/%s" % self.ticket1.pk,
                                   follow=True)
        self.assertTrue(
            response.redirect_chain[0][0].endswith("/member/tickets"))

        response = self.client.get(
            "/member/tickets/%s/cancel" % self.ticket1.pk, follow=True)
        self.assertTrue(
            response.redirect_chain[0][0].endswith("/member/tickets"))

    # def test_edit_ticket(self):
    #     """Test that we can edit tickets."""
    #     self.client.login(username=self.user.username, password="password")

    #     # First check link is visible on my tickets
    #     response = self.client.get("/member/tickets")
    #     future_ticket = response.soup.findAll("div", {"class": "ticket"})[1]
    #     edit_url = "/member/tickets/%s" % self.ticket2.pk
    #     self.assertIsNotNone(
    #         future_ticket.find("a", {"class": "button", "href": edit_url}))

    #     # Then POST to the link
    #     response = self.client.post(edit_url, {"quantity": 3})
    #     self.assertEqual(3, Ticket.objects.get(pk=self.ticket2.pk).number)

    def test_edit_another_users_ticket(self):
        """Test we can't edit tickets that don't belong to us."""
        user = mommy.make(settings.AUTH_USER_MODEL)
        user.set_password("password")
        user.save()

        edit_url = "/member/tickets/%s" % self.ticket2.pk

        self.client.login(username=user.username, password="password")
        response = self.client.post(edit_url, {"quantity": 3})
        self.assertEqual(404, response.status_code)
        self.assertEqual(5, Ticket.objects.get(pk=self.ticket2.pk).number)

    def test_cancel_ticket(self):
        """Test that we can cancel tickets."""
        self.client.login(username=self.user.username, password="password")

        # First check link is visible on my tickets
        response = self.client.get("/member/tickets")
        future_ticket = response.soup.findAll("div", {"class": "ticket"})[1]
        cancel_url = "/member/tickets/%s/cancel" % self.ticket2.pk
        self.assertIsNotNone(
            future_ticket.find("a", {"class": "button", "href": cancel_url}))

        # Then GET the link
        response = self.client.get(cancel_url)
        self.assertEqual(200, response.status_code)

        # Then POST to the link
        response = self.client.post(cancel_url)
        self.assertTrue(Ticket.objects.get(pk=self.ticket2.pk).cancelled)

    def test_cancel_another_users_ticket(self):
        """Test we can't cancel tickets that don't belong to us."""
        user = mommy.make(settings.AUTH_USER_MODEL)
        user.set_password("password")
        user.save()

        cancel_url = "/member/tickets/%s/cancel" % self.ticket2.pk

        self.client.login(username=user.username, password="password")

        # Then GET the link
        response = self.client.get(cancel_url)
        self.assertEqual(404, response.status_code)

        # Then POST to the link
        response = self.client.post(cancel_url)
        self.assertEqual(404, response.status_code)
        self.assertFalse(Ticket.objects.get(pk=self.ticket2.pk).cancelled)

    # def test_edit_ticket_quantity(self):
    #     """Test that the quantity for editing tickets is correct."""
    #     self.client.login(username=self.user.username, password="password")

    #     response = self.client.get("/member/tickets/%s" % self.ticket2.pk)
    #     quantity = response.soup.find("select", {"id": "id_quantity"})
    #     # self.assertEqual("30", quantity.findAll("option")[-1]["value"])

    #     self.ticket2.number = 15
    #     self.ticket2.save()

    #     response = self.client.get("/member/tickets/%s" % self.ticket2.pk)
    #     quantity = response.soup.find("select", {"id": "id_quantity"})
    #     self.assertEqual("30", quantity.findAll("option")[-1]["value"])

    #     mommy.make("Ticket", event=self.future_event, user=self.user,
    # number=5)

    #     response = self.client.get("/member/tickets/%s" % self.ticket2.pk)
    #     quantity = response.soup.find("select", {"id": "id_quantity"})
    #     self.assertEqual("25", quantity.findAll("option")[-1]["value"])
