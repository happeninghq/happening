""" Test ticket purchasing widget. """

from django_bs_test import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
import pytz


class TestTicketWidget(TestCase):

    """ Test ticket purchasing widget. """

    def test_remaining_tickets(self):
        """ Test that remaining_tickets works. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        self.assertIsNotNone(widget)
        tickets = widget.find("td", {"class": "remaining-tickets"}).text
        self.assertEqual("30 Tickets", tickets.strip())

        mommy.make("Ticket", event=event, number=1)
        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        tickets = widget.find("td", {"class": "remaining-tickets"}).text
        self.assertEqual("29 Tickets", tickets.strip())

        mommy.make("Ticket", event=event, number=5)
        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        tickets = widget.find("td", {"class": "remaining-tickets"}).text
        self.assertEqual("24 Tickets", tickets.strip())

        mommy.make("Ticket", event=event, number=23)
        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        tickets = widget.find("td", {"class": "remaining-tickets"}).text
        self.assertEqual("1 Ticket", tickets.strip())

    def test_end_date(self):
        """ Test that the end date is shown correctly. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        end_date = widget.find("td", {"class": "end-date"}).text
        self.assertEqual(event.datetime.strftime("%b. %d, %Y"),
                         end_date.strip())

    def test_past_event(self):
        """ Test that we can't buy tickets past the deadline. """
        mommy.make("Event", datetime=datetime.now(pytz.utc) -
                   timedelta(days=20), available_tickets=30)
        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        self.assertIsNone(widget)

    def test_quantity(self):
        """ Test that the quantity box doesn't allow > remainging tickets. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        self.assertEquals("30", widget.findAll("option")[-1]['value'])

        mommy.make("Ticket", event=event, number=5)
        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        self.assertEquals("25", widget.findAll("option")[-1]['value'])

    def test_sold_out(self):
        """ Test that we can't buy tickets once they are sold out. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                           timedelta(days=20), available_tickets=30)
        # First check that the register button is visible
        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        self.assertIsNotNone(widget.find("button"))

        mommy.make("Ticket", event=event, number=30)

        response = self.client.get("/")
        widget = response.soup.find(id="ticket-purchase")
        self.assertIsNone(widget.find("button"))
        self.assertIsNone(widget.find("option"))
        tickets = widget.find("td", {"class": "remaining-tickets"}).text
        self.assertEqual("Sold Out", tickets.strip())

