""" Test periodic tasks. """

from website.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz
from django.core import mail
from events.periodictasks import send_event_notifications


class TestPeriodicTasks(TestCase):

    """ Test periodic tasks. """

    def setUp(self):
        """ Set up a common user. """
        self.user = mommy.make("auth.User", email="test@example.com")

    def test_doesnt_send_reminder_more_than_one_week(self):
        """ Test that no reminder is sent more than 1 week in advance. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=8))
        event.buy_ticket(self.user, tickets=5)
        mail.outbox = []  # Remove purchase email
        send_event_notifications()
        self.assertEqual(0, len(mail.outbox))

    def test_doesnt_send_to_cancelled_tickets(self):
        """ Test that no reminder is sent for cancelled tickets. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=3))
        ticket = event.buy_ticket(self.user, tickets=5)
        ticket.cancel()
        mail.outbox = []  # Remove purchase/cancel emails
        send_event_notifications()
        self.assertEqual(0, len(mail.outbox))

    def test_sends_reminder_email_one_week_in_advance(self):
        """ Test that the 1 week reminder is sent. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=6))
        event.buy_ticket(self.user, tickets=5)
        mail.outbox = []  # Remove purchase email
        send_event_notifications()
        self.assertEqual(1, len(mail.outbox))
        self.assertTrue(str(event) in mail.outbox[0].body)
        self.assertTrue("in 5 days" in mail.outbox[0].body)

    def test_sends_reminder_email_one_day_in_advance(self):
        """ Test that the 1 day reminder is sent. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(hours=26))
        event.buy_ticket(self.user, tickets=5)
        mail.outbox = []  # Remove purchase email
        send_event_notifications()
        self.assertEqual(1, len(mail.outbox))
        self.assertTrue(str(event) in mail.outbox[0].body)
        self.assertTrue("in a day" in mail.outbox[0].body)

    def test_sends_only_single_email_at_a_time(self):
        """ Test that it will only send the most recent notification. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=6))
        event.buy_ticket(self.user, tickets=5)
        mail.outbox = []  # Remove purchase email
        send_event_notifications()
        self.assertEqual(1, len(mail.outbox))
        self.assertTrue(str(event) in mail.outbox[0].body)
        self.assertTrue("in 5 days" in mail.outbox[0].body)

    def test_sends_emails_to_all_attendees(self):
        """ Test that multiple attendees recieve the emails. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=6))
        user2 = mommy.make("auth.User", email="test2@example.com")
        event.buy_ticket(self.user)
        event.buy_ticket(user2)
        mail.outbox = []  # Remove purchase emails
        send_event_notifications()
        self.assertEqual(2, len(mail.outbox))

    def test_only_sends_reminder_for_future_events(self):
        """ Test that past events do not trigger emails. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=1))
        event.buy_ticket(self.user, tickets=5)
        mail.outbox = []  # Remove purchase email
        event.datetime = datetime.now(pytz.utc) - timedelta(days=1)
        event.save()
        send_event_notifications()
        self.assertEqual(0, len(mail.outbox))

    def test_only_sends_one_email_at_a_time(self):
        """ Test that repeated send_event_notifications will not stack. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=1))
        event.buy_ticket(self.user, tickets=5)
        mail.outbox = []  # Remove purchase email
        send_event_notifications()
        self.assertEqual(1, len(mail.outbox))
        mail.outbox = []  # Remove purchase email
        send_event_notifications()
        self.assertEqual(0, len(mail.outbox))

    def test_only_sends_one_notification_for_multiple_purchases(self):
        """ Test that one user with two purchases only recieves one email. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=6))
        event.buy_ticket(self.user, tickets=5)
        mail.outbox = []  # Remove purchase email
        send_event_notifications()
        event.buy_ticket(self.user, tickets=5)
        mail.outbox = []  # Remove purchase email
        send_event_notifications()
        self.assertEqual(0, len(mail.outbox))
