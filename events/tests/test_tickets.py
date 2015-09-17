"""Test ticket purchasing."""

from events.exceptions import EventFinishedError, NoTicketsError
from unittest import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from django.core import mail
from django.conf import settings


class TestTickets(TestCase):

    """Test ticket purchasing."""

    def test_remaining_tickets(self):
        """Test that remaining_tickets works."""
        event = mommy.make("Event")
        self.assertEqual(event.available_tickets, event.remaining_tickets)
        mommy.make("Ticket", event=event)
        self.assertEqual(event.available_tickets - 1, event.remaining_tickets)
        mommy.make("Ticket", event=event)
        mommy.make("Ticket", event=event)
        mommy.make("Ticket", event=event)
        mommy.make("Ticket", event=event)
        mommy.make("Ticket", event=event)
        self.assertEqual(event.available_tickets - 6, event.remaining_tickets)

    def test_buy_tickets(self):
        """Test that we can buy tickets."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        user = mommy.make(settings.AUTH_USER_MODEL)
        self.assertEqual(30, event.remaining_tickets)
        event.buy_ticket(user)  # Should buy 1 ticket
        self.assertEqual(29, event.remaining_tickets)

        ticket = event.buy_ticket(user, tickets=3)  # Should buy 3 ticket
        self.assertEqual(26, event.remaining_tickets)

        # Test that the purchase date is recorded
        self.assertIsNotNone(ticket.purchased_datetime)

    def test_buy_passed_deadline(self):
        """Test that we can't buy tickets past the deadline."""
        past_event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                timedelta(days=20), available_tickets=30)
        user = mommy.make(settings.AUTH_USER_MODEL)

        with self.assertRaises(EventFinishedError):
            past_event.buy_ticket(user)

        self.assertEqual(30, past_event.remaining_tickets)

    def test_buy_tickets_sold_out(self):
        """Test that we can't buy tickets once they are sold out."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=1)
        user = mommy.make(settings.AUTH_USER_MODEL)

        event.buy_ticket(user)  # This should be the last ticket

        self.assertEqual(0, event.remaining_tickets)

        with self.assertRaises(NoTicketsError):
            event.buy_ticket(user)

        self.assertEqual(0, event.remaining_tickets)

    def test_cancel_tickets(self):
        """Test that we can cancel tickets."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        user = mommy.make(settings.AUTH_USER_MODEL)

        order = event.buy_ticket(user, tickets=5)

        self.assertEqual(25, event.remaining_tickets)

        mail.outbox = []

        order.tickets.first().cancel()

        self.assertEqual(1, len(mail.outbox))

        self.assertEqual(26, event.remaining_tickets)
        # Test that the cancellation date is recorded
        self.assertIsNotNone(order.tickets.first().cancelled_datetime)

        # Test that we can't cancel tickets passed the deadline
        order = event.buy_ticket(user, tickets=5)
        event.start = datetime.now(pytz.utc) - timedelta(days=20)
        event.save()

        with self.assertRaises(EventFinishedError):
            order.tickets.first().cancel()

        self.assertIsNone(order.tickets.first().cancelled_datetime)
        self.assertFalse(order.tickets.first().cancelled)
