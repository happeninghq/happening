""" Test ticket purchasing. """

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from django.core import mail
from events.exceptions import NoTicketsError
from django.conf import settings


class TestTicketPurchase(TestCase):

    """ Test ticket purchasing. """

    def setUp(self):
        """ Set up a common user. """
        self.user = mommy.make(settings.AUTH_USER_MODEL,
                               email="test@example.com")
        self.user.set_password("password")
        self.user.save()

    def test_buy_ticket_method(self):
        """ Test that buy_ticket doesn't allow us too many tickets. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        with self.assertRaises(NoTicketsError):
            event.buy_ticket(self.user, tickets=31)

    def test_purchase_requires_login(self):
        """ Test you need to be logged in to purchase tickets. """
        past_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                timedelta(days=20))
        response = self.client.get(
            "/events/%s/purchase_tickets" % past_event.pk, follow=True)
        self.assertTrue("accounts/login" in response.redirect_chain[0][0])

    def test_past_event(self):
        """ Test that we can't buy tickets past the deadline. """
        past_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                timedelta(days=20))
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            "/events/%s/purchase_tickets" % past_event.pk, follow=True)
        self.assertTrue(
            response.redirect_chain[0][0].endswith(
                "/events/%s" % past_event.pk))

    def test_quantity(self):
        """ Test that the quantity box doesn't allow > remainging tickets. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/events/%s/purchase_tickets" % event.pk)
        quantity = response.soup.find(id="id_quantity")
        highest_value = quantity.findAll("option")[-1]["value"]
        self.assertEquals("30", highest_value)

        event.buy_ticket(self.user, tickets=5)

        response = self.client.get("/events/%s/purchase_tickets" % event.pk)
        quantity = response.soup.find(id="id_quantity")
        highest_value = quantity.findAll("option")[-1]["value"]
        self.assertEquals("25", highest_value)

    def test_sold_out(self):
        """ Test that we can't buy tickets once they are sold out. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        self.client.login(username=self.user.username, password="password")
        event.buy_ticket(self.user, tickets=30)

        response = self.client.get("/events/%s/purchase_tickets" % event.pk,
                                   follow=True)
        self.assertTrue(
            response.redirect_chain[0][0].endswith(
                "/events/%s" % event.pk))

    def test_purchase(self):
        """ Test that a purchase creates a ticket and redirects. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            "/events/%s/purchase_tickets" % event.pk,
            {"quantity": 5},
            follow=True)
        self.assertTrue(
            "events/tickets_purchased" in response.redirect_chain[0][0])
        self.assertEquals(self.user.tickets.first(),
                          response.context["ticket"])
        self.assertEquals(event.tickets.first(), response.context["ticket"])

    def test_cant_view_others_confirmation(self):
        """ Test that users can only view their own order confirmations. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)

        user2 = mommy.make(settings.AUTH_USER_MODEL)
        user2.set_password("password")
        user2.save()

        ticket = event.buy_ticket(self.user, tickets=5)

        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/events/tickets_purchased/%s" % ticket.pk)
        self.assertEquals(200, response.status_code)

        self.client.login(username=user2.username, password="password")

        response = self.client.get("/events/tickets_purchased/%s" % ticket.pk)
        self.assertEquals(404, response.status_code)

    def test_ticket_purchase_sends_confirmation_email(self):
        """ Test that we send a confirmation email after purchasing ticket. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            "/events/%s/purchase_tickets" % event.pk,
            {"quantity": 5},
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

    def test_ticket_purchase_sends_extra_notifications_notification_1(self):
        """ Test that the one week notification is sent when needed. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=4), available_tickets=30)
        event.buy_ticket(self.user)
        # We should just have the purchase email as this event hasn't
        # sent notifications yet
        self.assertEqual(1, len(mail.outbox))

        mail.outbox = []  # Clear previous purchase notification

        event2 = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                            timedelta(days=4), available_tickets=30,
                            upcoming_notification_1_sent=True)
        event2.buy_ticket(self.user)

        # Purchase email and notification email
        self.assertEqual(2, len(mail.outbox))
        self.assertTrue(str(event2) in mail.outbox[1].body)

        event2.buy_ticket(self.user)
        # Should only recieve one additional email (no more notification)
        self.assertEqual(3, len(mail.outbox))

    def test_ticket_purchase_sends_extra_notifications_notification_2(self):
        """ Test that the one day notification is sent when needed. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(hours=7), available_tickets=30)
        event.buy_ticket(self.user)
        # We should just have the purchase email as this event hasn't
        # sent notifications yet
        self.assertEqual(1, len(mail.outbox))

        mail.outbox = []  # Clear previous purchase notification

        event2 = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                            timedelta(days=4), available_tickets=30,
                            upcoming_notification_1_sent=True)
        event2.buy_ticket(self.user)

        # Purchase email and notification email
        self.assertEqual(2, len(mail.outbox))
        self.assertTrue(str(event2) in mail.outbox[1].body)

        event2.buy_ticket(self.user)
        # Should only recieve one additional email (no more notification)
        self.assertEqual(3, len(mail.outbox))
