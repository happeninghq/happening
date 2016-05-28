"""Test waiting list."""

from happening.tests import TestCase
from model_mommy import mommy
from django.conf import settings
import pytz
from datetime import datetime, timedelta
import json


class TestWaitingList(TestCase):

    """Test waiting list."""

    def setUp(self):
        """Set up a common user."""
        super(TestWaitingList, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL,
                               email="test@example.com")
        self.user.set_password("password")
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        self.event = mommy.make("Event", start=datetime.now(pytz.utc) +
                                timedelta(days=20))

        self.ticket_type = mommy.make("TicketType", event=self.event,
                                      number=30, visible=True,
                                      waiting_list_enabled=True)

    def test_waiting_list(self):
        """Test that we can join and leave waiting lists."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/events/%s" % self.event.id)
        self.assertFalse("Waiting Lists" in str(response.soup))

        self.ticket_type.number = 0
        self.ticket_type.save()

        response = self.client.get("/events/%s" % self.event.id)

        self.assertTrue("Waiting Lists" in str(response.soup))
        self.assertEqual(response.soup.find("span", class_="waiting").text,
                         "0")

        # Join the waiting list
        response = self.client.post("/events/%s/wait" % self.ticket_type.id)

        response = self.client.get("/events/%s" % self.event.id)
        self.assertEqual(response.soup.find("span", class_="waiting").text,
                         "1")

        # Leave the waiting list
        response = self.client.post("/events/%s/wait/leave" %
                                    self.ticket_type.id)

        response = self.client.get("/events/%s" % self.event.id)
        self.assertEqual(response.soup.find("span", class_="waiting").text,
                         "0")

    def test_waiting_list_not_shown_in_past(self):
        """Test that waiitng lists only work for future events."""
        self.event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                timedelta(days=20))
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/events/%s" % self.event.id)
        self.assertFalse("Waiting Lists" in str(response.soup))

        self.ticket_type.number = 0
        self.ticket_type.save()

        response = self.client.get("/events/%s" % self.event.id)

        self.assertFalse("Waiting Lists" in str(response.soup))

    def test_new_ticket_is_held(self):
        """Test that a new ticket is not available to purchase."""
        self.client.login(username=self.user.username, password="password")

        self.ticket_type.number = 0
        self.ticket_type.save()

        # Join the waiting list
        self.client.post("/events/%s/wait" % self.ticket_type.id)

        # Create a ticket
        self.ticket_type.number = 1
        self.ticket_type.save()

        # Check that a person on the waiting list can't see the ticket
        response = self.client.get("/events/%s" % self.event.id)

        tickets = json.loads(response.soup.find("form",
                             class_="purchase-tickets-widget")[
                             "data-active-tickets"])

        self.assertEqual(tickets[0]["remaining_tickets"], 0)

        # Check they can't purchase
        # TODO

        # Check others can't see the ticket
        client2 = self.create_client()
        client2.get("/events/%s" % self.event.id)

        tickets = json.loads(response.soup.find("form",
                             class_="purchase-tickets-widget")[
                             "data-active-tickets"])

        self.assertEqual(tickets[0]["remaining_tickets"], 0)

    def test_cancelled_ticket_is_held(self):
        """Test that a cancelled ticket is not available for purchase."""
        pass

    def test_manually_offer_ticket(self):
        """Test that admins can manually offer a ticket for sale."""
        self.client.login(username=self.user.username, password="password")

        self.ticket_type.number = 0
        self.ticket_type.save()

        # Join the waiting list
        self.client.post("/events/%s/wait" % self.ticket_type.id)

        # Create a ticket
        self.ticket_type.number = 1
        self.ticket_type.save()

        # Release the ticket to the waiting user
        self.client.post("/staff/events/waiting-lists/%s/release/%s" % (
            self.ticket_type.id, self.user.id))

        # Check that a person on the waiting list can see the ticket
        response = self.client.get("/events/%s" % self.event.id)

        tickets = json.loads(response.soup.find("form",
                             class_="purchase-tickets-widget")[
                             "data-active-tickets"])

        self.assertEqual(tickets[0]["remaining_tickets"], 1)

        # Check they can purchase the ticket
        # TODO

        # Check that a person not on the waiting list can't
        client2 = self.create_client()
        response = client2.get("/events/%s" % self.event.id)

        tickets = json.loads(response.soup.find("form",
                             class_="purchase-tickets-widget")[
                             "data-active-tickets"])

        self.assertEqual(tickets[0]["remaining_tickets"], 0)

    def test_automatically_offer_ticket(self):
        """Test that tickets are automatically offered for sale."""
        pass

    def test_waiting_list_is_retracted_when_sold_out(self):
        """Test that offers are retracted when sold out."""
        user2 = mommy.make(settings.AUTH_USER_MODEL,
                           email="test2@example.com")
        user2.set_password("password")
        user2.save()

        client2 = self.create_client()

        self.client.login(username=self.user.username, password="password")
        client2.login(username=user2.username, password="password")

        # Both clients logged in - now get both of them on the waiting list

        self.ticket_type.number = 0
        self.ticket_type.save()

        self.client.post("/events/%s/wait" % self.ticket_type.id)
        client2.post("/events/%s/wait" % self.ticket_type.id)

        # Release tickets to both
        self.ticket_type.number = 1
        self.ticket_type.save()

        self.client.post("/staff/events/waiting-lists/%s/release/%s" % (
            self.ticket_type.id, self.user.id))
        self.client.post("/staff/events/waiting-lists/%s/release/%s" % (
            self.ticket_type.id, user2.id))

        subscription = self.ticket_type.waiting_list_subscriptions.filter(
            user=user2).first()

        self.assertTrue(subscription.can_purchase)

        # Now user 1 buys the ticket, so user 2 should have their access
        # revoked

        self.event.buy_tickets(self.user, {self.ticket_type.pk: 1})
        subscription = self.ticket_type.waiting_list_subscriptions.filter(
            user=user2).first()
        self.assertFalse(subscription.can_purchase)
