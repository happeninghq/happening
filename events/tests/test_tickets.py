""" Test ticket purchasing. """

from unittest import TestCase
from model_mommy import mommy


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
