""" Test event view. """

from website.tests import TestCase
from model_mommy import mommy, generators
from datetime import datetime, timedelta
import pytz


class TestEventView(TestCase):

    """ Test Event View. """

    def test_nonexisting_event(self):
        """ Test view for event which doesn't exist. """
        response = self.client.get("/events/1")
        self.assertEquals(response.status_code, 404)

    def test_future_event(self):
        """ Test view for an event in the future. """
        future_event = mommy.make("Event", datetime=datetime.now(pytz.utc) +
                                  timedelta(days=20), available_tickets=30)
        response = self.client.get("/events/%s" % future_event.id)
        self.assertEquals(response.status_code, 200)
        widget = response.soup.find("div", {"class": "ticket-purchase"})
        self.assertIsNotNone(widget)
        tickets = widget.find("td", {"class": "remaining-tickets"}).text
        self.assertEqual("30 Tickets", tickets.strip())

    def test_past_event(self):
        """ Test view for an event in the past. """
        empty_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                 timedelta(days=20))
        filled_event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                                  timedelta(days=20),
                                  sponsor=mommy.make("Sponsor"),
                                  challenge_text=generators.gen_text(),
                                  solution_text=generators.gen_text(),
                                  image=generators.gen_image_field())
        empty_response = self.client.get("/events/%s" % empty_event.id)
        filled_response = self.client.get("/events/%s" % filled_event.id)
        self.assertEquals(empty_response.status_code, 200)
        self.assertEquals(filled_response.status_code, 200)

        # Check heading
        self.assertEquals(empty_event.heading(),
                          empty_response.soup.find("h2").text)
        self.assertEquals(filled_event.heading(),
                          filled_response.soup.find("h2").text)

        # Check challenge text
        self.assertIsNone(empty_response.soup.find(id="challenge-text"))
        self.assertEquals(filled_event.challenge_text.strip(),
                          filled_response.soup.find(id="challenge-text")
                                              .text.strip())

        # Check solutions photo
        self.assertIsNone(empty_response.soup.find(id="event-image"))
        self.assertEquals(filled_event.image.url,
                          filled_response.soup.find(id="event-image")
                                              .find("img")['src'])

        # Check solutions text
        self.assertIsNone(empty_response.soup.find(id="solution-text"))
        self.assertEquals(filled_event.solution_text.strip(),
                          filled_response.soup.find(id="solution-text")
                                              .text.strip())

    def test_event_solutions(self):
        """ Test that the view shows the correct event solutions. """
        event = mommy.make("Event", datetime=datetime.now(pytz.utc) -
                           timedelta(days=20))

        # No solutions should have no list
        response = self.client.get("/events/%s" % event.id)
        self.assertIsNone(response.soup.find(id="event-solutions"))

        # Create a solution, ensure it appears in the list
        mommy.make("EventSolution", event=event)
        response = self.client.get("/events/%s" % event.id)
        self.assertIsNotNone(response.soup.find(id="event-solutions"))
        self.assertEqual(1, len(response.soup.find(id="event-solutions")
                                .findAll("tr")))

        mommy.make("EventSolution", event=event)
        response = self.client.get("/events/%s" % event.id)
        self.assertEqual(2, len(response.soup.find(id="event-solutions")
                                .findAll("tr")))
