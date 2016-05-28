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
        ticket_type = mommy.make("TicketType", event=event, number=30,
                                 visible=True)

        self.assertEqual(ticket_type.number, ticket_type.remaining_tickets)
        mommy.make("Ticket", event=event, type=ticket_type)
        self.assertEqual(ticket_type.number - 1,
                         ticket_type.remaining_tickets)
        mommy.make("Ticket", event=event, type=ticket_type)
        mommy.make("Ticket", event=event, type=ticket_type)
        mommy.make("Ticket", event=event, type=ticket_type)
        mommy.make("Ticket", event=event, type=ticket_type)
        mommy.make("Ticket", event=event, type=ticket_type)
        self.assertEqual(ticket_type.number - 6,
                         ticket_type.remaining_tickets)

    def test_buy_tickets(self):
        """Test that we can buy tickets."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20))
        ticket_type = mommy.make("TicketType", event=event, number=30,
                                 visible=True)
        user = mommy.make(settings.AUTH_USER_MODEL)
        self.assertEqual(30, ticket_type.remaining_tickets)

        # Should buy 3 tickets
        order = event.buy_tickets(user, {ticket_type.pk: 3})
        self.assertEqual(27, ticket_type.remaining_tickets)

        # Test that the purchase date is recorded
        self.assertIsNotNone(order.purchased_datetime)

    def test_buy_passed_deadline(self):
        """Test that we can't buy tickets past the deadline."""
        past_event = mommy.make("Event", start=datetime.now(pytz.utc) -
                                timedelta(days=20))
        ticket_type = mommy.make("TicketType", event=past_event, number=30,
                                 visible=True)
        user = mommy.make(settings.AUTH_USER_MODEL)

        with self.assertRaises(EventFinishedError):
            past_event.buy_tickets(user, {ticket_type.pk: 1})

        self.assertEqual(30, ticket_type.remaining_tickets)

    def test_buy_tickets_sold_out(self):
        """Test that we can't buy tickets once they are sold out."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20))
        ticket_type = mommy.make("TicketType", event=event, number=1,
                                 visible=True)
        user = mommy.make(settings.AUTH_USER_MODEL)

        # This should be the last ticket
        event.buy_tickets(user, {ticket_type.pk: 1})

        self.assertEqual(0, ticket_type.remaining_tickets)

        with self.assertRaises(NoTicketsError):
            event.buy_tickets(user, {ticket_type.pk: 1})

        self.assertEqual(0, ticket_type.remaining_tickets)

    def test_cancel_tickets(self):
        """Test that we can cancel tickets."""
        event = mommy.make("Event", start=datetime.now(pytz.utc) +
                           timedelta(days=20))
        ticket_type = mommy.make("TicketType", event=event, number=30,
                                 visible=True)
        user = mommy.make(settings.AUTH_USER_MODEL)

        order = event.buy_tickets(user, {ticket_type.pk: 5})

        self.assertEqual(25, ticket_type.remaining_tickets)

        mail.outbox = []

        order.tickets.first().cancel()

        self.assertEqual(1, len(mail.outbox))

        self.assertEqual(26, ticket_type.remaining_tickets)
        # Test that the cancellation date is recorded
        self.assertIsNotNone(order.tickets.first().cancelled_datetime)

        # Test that we can't cancel tickets passed the deadline
        order = event.buy_tickets(user, {ticket_type.pk: 5})
        event.start = datetime.now(pytz.utc) - timedelta(days=20)
        event.save()

        with self.assertRaises(EventFinishedError):
            order.tickets.first().cancel()

        self.assertIsNone(order.tickets.first().cancelled_datetime)
        self.assertFalse(order.tickets.first().cancelled)
