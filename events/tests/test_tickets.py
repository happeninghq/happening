""" Test ticket purchasing. """

from events.exceptions import EventFinishedError, NoTicketsError
from events.exceptions import TicketCancelledError
from unittest import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from django.core import mail


class TestTickets(TestCase):

    """ Test ticket purchasing. """

    def test_remaining_tickets(self):
        """ Test that remaining_tickets works. """
        event = mommy.make("Event")
        self.assertEqual(event.available_tickets, event.remaining_tickets)
        mommy.make("Ticket", event=event, number=1)
        self.assertEqual(event.available_tickets - 1, event.remaining_tickets)
        mommy.make("Ticket", event=event, number=5)
        self.assertEqual(event.available_tickets - 6, event.remaining_tickets)

    def test_buy_tickets(self):
        """ Test that we can buy tickets. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        user = mommy.make("auth.User")
        self.assertEqual(30, event.remaining_tickets)
        event.buy_ticket(user)  # Should buy 1 ticket
        self.assertEqual(29, event.remaining_tickets)

        ticket = event.buy_ticket(user, tickets=3)  # Should buy 3 ticket
        self.assertEqual(26, event.remaining_tickets)

        # Test that the purchase date is recorded
        self.assertIsNotNone(ticket.purchased_datetime)

    def test_buy_passed_deadline(self):
        """ Test that we can't buy tickets past the deadline. """
        past_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                timedelta(days=20), available_tickets=30)
        user = mommy.make("auth.User")

        with self.assertRaises(EventFinishedError):
            past_event.buy_ticket(user)

        self.assertEqual(30, past_event.remaining_tickets)

    def test_buy_tickets_sold_out(self):
        """ Test that we can't buy tickets once they are sold out. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=1)
        user = mommy.make("auth.User")

        event.buy_ticket(user)  # This should be the last ticket

        self.assertEqual(0, event.remaining_tickets)

        with self.assertRaises(NoTicketsError):
            event.buy_ticket(user)

        self.assertEqual(0, event.remaining_tickets)

    def test_edit_tickets(self):
        """ Test that we can edit tickets. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        user = mommy.make("auth.User")

        ticket = event.buy_ticket(user, tickets=5)

        self.assertEqual(25, event.remaining_tickets)

        mail.outbox = []

        ticket.change_number(1)

        self.assertEqual(1, len(mail.outbox))

        self.assertEqual(29, event.remaining_tickets)

        # Test that we can't edit our number bigger than available tickets
        ticket.change_number(30)
        self.assertEqual(0, event.remaining_tickets)

        ticket.change_number(5)

        with self.assertRaises(NoTicketsError):
            ticket.change_number(31)

        # Test that we can't edit tickets passed the deadline

        event.datetime = datetime.now(pytz.utc) - timedelta(days=20)
        event.save()

        with self.assertRaises(EventFinishedError):
            ticket.change_number(3)

    def test_edit_tickets_zero(self):
        """ Test editing a ticket to 0 cancels it. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        user = mommy.make("auth.User")

        ticket = event.buy_ticket(user, tickets=5)

        self.assertEqual(25, event.remaining_tickets)

        ticket.change_number(0)

        self.assertEqual(30, event.remaining_tickets)
        self.assertTrue(ticket.cancelled)

    def test_edit_cancelled_ticket(self):
        """ Test editing a cancelled ticket. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        user = mommy.make("auth.User")

        ticket = event.buy_ticket(user, tickets=5)
        ticket.cancel()

        with self.assertRaises(TicketCancelledError):
            ticket.change_number(3)

    def test_cancel_tickets(self):
        """ Test that we can cancel tickets. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        user = mommy.make("auth.User")

        ticket = event.buy_ticket(user, tickets=5)

        self.assertEqual(25, event.remaining_tickets)

        mail.outbox = []

        ticket.cancel()

        self.assertEqual(1, len(mail.outbox))

        self.assertEqual(30, event.remaining_tickets)
        # Test that the cancellation date is recorded
        self.assertIsNotNone(ticket.cancelled_datetime)

        # Test that we can't cancel tickets passed the deadline
        ticket = event.buy_ticket(user, tickets=5)
        event.datetime = datetime.now(pytz.utc) - timedelta(days=20)
        event.save()

        with self.assertRaises(EventFinishedError):
            ticket.cancel()

        self.assertIsNone(ticket.cancelled_datetime)
        self.assertFalse(ticket.cancelled)
