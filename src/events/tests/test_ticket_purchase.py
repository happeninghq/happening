"""Test ticket purchasing."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from django.core import mail
from events.exceptions import NoTicketsError
from django.conf import settings


class TestTicketPurchase(TestCase):

    """Test ticket purchasing."""

    def setUp(self):
        """Set up a common user."""
        super(TestTicketPurchase, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL,
                               email="test@example.com")
        self.user.set_password("password")
        self.user.save()

    def test_buy_ticket_method(self):
        """Test that buy_ticket doesn't allow us too many tickets."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20))
        ticket_type = mommy.make("TicketType", event=event, number=30,
                                 visible=True)
        with self.assertRaises(NoTicketsError):
            event.buy_tickets(self.user, {ticket_type.pk: 31})

    def test_purchase_requires_login(self):
        """Test you need to be logged in to purchase tickets."""
        past_event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                timedelta(days=20))
        response = self.client.get(
            "/events/%s/purchase_tickets" % past_event.pk, follow=True)
        self.assertTrue("accounts/login" in response.redirect_chain[0][0])

    def test_past_event(self):
        """Test that we can't buy tickets past the deadline."""
        past_event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                timedelta(days=20))
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            "/events/%s/purchase_tickets" % past_event.pk, follow=True)
        self.assertTrue(
            response.redirect_chain[0][0].endswith(
                "/events/%s" % past_event.pk))

    def test_sold_out(self):
        """Test that we can't buy tickets once they are sold out."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20))
        ticket_type = mommy.make("TicketType", event=event, number=30,
                                 visible=True)

        self.client.login(username=self.user.username, password="password")
        event.buy_tickets(self.user, {ticket_type.pk: 30})

        response = self.client.get("/events/%s/purchase_tickets" % event.pk,
                                   follow=True)
        self.assertTrue(
            response.redirect_chain[0][0].endswith(
                "/events/%s" % event.pk))

    def test_purchase(self):
        """Test that a purchase creates a ticket and redirects."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20))
        ticket_type = mommy.make("TicketType", event=event, number=30, price=0,
                                 visible=True)
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            "/events/%s/purchase_tickets" % event.pk,
            {"tickets_" + str(ticket_type.pk): 1},
            follow=True)
        self.assertTrue(
            "events/tickets_purchased" in response.redirect_chain[0][0])

        # For some reason ["order"] is getting set to a dict - NO IDEA WHY
        # So for now just use ticket.order
        self.assertEqual(self.user.orders.first(),
                         response.context["ticket"].order)
        self.assertEqual(event.orders.first(), response.context["ticket"].order)

    def test_cant_view_others_confirmation(self):
        """Test that users can only view their own order confirmations."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20))
        ticket_type = mommy.make("TicketType", event=event, number=30,
                                 visible=True)

        user2 = mommy.make(settings.AUTH_USER_MODEL)
        user2.set_password("password")
        user2.save()

        ticket = event.buy_tickets(self.user, {ticket_type.pk: 5})

        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/events/tickets_purchased/%s" % ticket.pk)
        self.assertEqual(200, response.status_code)

        self.client.login(username=user2.username, password="password")

        response = self.client.get("/events/tickets_purchased/%s" % ticket.pk)
        self.assertEqual(404, response.status_code)

    def test_ticket_purchase_sends_confirmation_email(self):
        """Test that we send a confirmation email after purchasing ticket."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20))
        ticket_type = mommy.make("TicketType", event=event, number=30,
                                 visible=True, price=0)
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            "/events/%s/purchase_tickets" % event.pk,
            {"tickets_" + str(ticket_type.pk): 1},
            follow=True)
        self.assertTrue(
            "events/tickets_purchased" in response.redirect_chain[0][0])

        self.assertEqual(1, len(mail.outbox))

        # Addressed to the user
        self.assertTrue(str(self.user) in mail.outbox[0].body)
        self.assertEqual("test@example.com", mail.outbox[0].to[0])
        self.assertEqual(1, len(mail.outbox[0].to))

        # Mentions the event
        self.assertTrue(str(event) in mail.outbox[0].body)
        self.assertTrue(str(event) in mail.outbox[0].subject)
