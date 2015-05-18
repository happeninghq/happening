"""Test administrating events."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
from events.models import Event
import pytz
from uuid import uuid4
from django.core import mail
from django.conf import settings


class TestEvents(TestCase):

    """Test administrating events."""

    def setUp(self):
        """Set up a user."""
        self.user = mommy.make(settings.AUTH_USER_MODEL, is_staff=True)
        self.user.set_password("password")
        self.user.save()

        self.event = mommy.make("Event", start=datetime.now(pytz.utc) +
                                timedelta(days=2), available_tickets=30)

    def test_send_email(self):
        """Test that administrators can send emails to attending members."""
        test_subject = uuid4().hex
        test_content = uuid4().hex
        # With a single attendee
        mommy.make("Ticket", event=self.event, number=1)
        self.client.login(username=self.user.username, password="password")

        self.client.post("/staff/events/%s/email" % self.event.id, {
            "subject": test_subject,
            "content": test_content
            })

        self.assertEquals(1, len(mail.outbox))
        self.assertEquals(test_subject, mail.outbox[0].subject)
        self.assertTrue(test_content in mail.outbox[0].body)
        mail.outbox = []

        # With two attendees
        mommy.make("Ticket", event=self.event, number=1)
        self.client.post("/staff/events/%s/email" % self.event.id, {
            "subject": test_subject,
            "content": test_content
            })
        self.assertEquals(2, len(mail.outbox))

    def test_events(self):
        """Test listing events."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/staff/events")
        # We should have the title row and then 1 row for an event
        self.assertEquals(2, len(response.soup.find("table").findAll("tr")))
        for i in range(10):
            mommy.make("Event", start=datetime.now(pytz.utc) +
                       timedelta(days=i), available_tickets=30)

        response = self.client.get("/staff/events")
        # We only show up to 10 per page
        self.assertEquals(12, len(response.soup.find("table").findAll("tr")))

    def test_event(self):
        """Test viewing an event page."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/staff/events/%s" % self.event.id)

        # Check that no tickets are listed
        self.assertEquals(1, len(response.soup.find("table").findAll("tr")))

        mommy.make("Ticket", event=self.event, user=self.user, number=1)

        # Check it lists the ticket
        response = self.client.get("/staff/events/%s" % self.event.id)
        self.assertEquals(2, len(response.soup.find("table").findAll("tr")))

    def test_edit_event(self):
        """Test editing events."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/staff/events/%s/edit" % self.event.id)

        # Check that information is being loaded into the form
        self.assertEquals(self.event.title, response.soup.find("input",
                          {"id": "id_title"})["value"])

        response = self.client.post("/staff/events/%s/edit" % self.event.id, {
            "title": "NEW TITLE",
            "start": "2010-05-05 19:00:00",
            "available_tickets": "30",
            "challenge_language": "",
            "challenge_title": "",
            "challenge_text": "",
            "solution_text": "",

            # TODO: These two shouldn't be tested here
            "ticket_purchased_message": ".",
            "description": "."
        }, follow=True)
        self.assertTrue("/staff/events/%s" % self.event.id in
                        response.redirect_chain[0][0])

        self.event = Event.objects.get(pk=self.event.pk)
        self.assertEquals(self.event.title, "NEW TITLE")

    def test_create_event(self):
        """Test creating events."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/staff/events/create")

        response = self.client.post("/staff/events/create", {
            "title": "NEW TITLE",
            "start": "2010-05-05 19:00:00",
            "available_tickets": "30",
            "challenge_language": "",
            "challenge_title": "",
            "challenge_text": "",
            "solution_text": "",

            # TODO: These two shouldn't be tested here
            "ticket_purchased_message": ".",
            "description": "."
        }, follow=True)
        self.assertTrue("/staff/events" in
                        response.redirect_chain[0][0])

        event = Event.objects.get(pk=2)
        self.assertEquals(event.title, "NEW TITLE")

    def test_add_attendee(self):
        """Test adding an attendee after an event begins."""
        second_user = mommy.make(settings.AUTH_USER_MODEL)

        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/staff/events/%s" % self.event.id)

        self.assertIsNotNone(
            response.soup.find(
                "a",
                {"href": "/staff/events/%s/add_attendee" % self.event.id}))

        response = self.client.get(
            "/staff/events/%s/add_attendee" % self.event.id)

        trs = response.soup.find("table").findAll("tr")

        # This should list all users who haven't got tickets
        self.assertEquals(3, len(trs))

        # (Header + staff + not staff)

        response = self.client.post(
            "/staff/events/%s/add_attendee" % self.event.id,
            {
                "member_pk": self.user.pk
            }, follow=True)

        self.assertTrue("/staff/events/%s" % self.event.id in
                        response.redirect_chain[0][0])

        self.assertEquals(2, len(response.soup.find("table").findAll("tr")))

        response = self.client.post(
            "/staff/events/%s/add_attendee" % self.event.id,
            {
                "member_pk": second_user.pk
            }, follow=True)

        self.assertTrue("/staff/events/%s" % self.event.id in
                        response.redirect_chain[0][0])

        self.assertEquals(3, len(response.soup.find("table").findAll("tr")))

    def test_check_in(self):
        """Test checking in."""
        self.client.login(username=self.user.username, password="password")

        mommy.make("Ticket", event=self.event, user=self.user, number=1)

        # Check it lists the ticket
        response = self.client.get("/staff/events/%s" % self.event.id)
        trs = response.soup.find("table").findAll("tr")
        self.assertEquals(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Check Out")

        self.assertIsNotNone(check_in_button)
        self.assertIsNone(check_out_button)

        response = self.client.get(check_in_button['href'], follow=True)
        # This should check them in then redirect back

        trs = response.soup.find("table").findAll("tr")
        self.assertEquals(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Cancel Check In")

        self.assertIsNone(check_in_button)
        self.assertIsNotNone(check_out_button)

        response = self.client.get(check_out_button['href'], follow=True)
        # This will check them out then redirect back

        trs = response.soup.find("table").findAll("tr")
        self.assertEquals(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Cancel Check In")

        self.assertIsNotNone(check_in_button)
        self.assertIsNone(check_out_button)

    def test_manage_check_ins(self):
        """Test checking in using dedicated page."""
        self.client.login(username=self.user.username, password="password")

        mommy.make("Ticket", event=self.event, user=self.user, number=1)

        # Check it lists the ticket
        response = self.client.get(
            "/staff/events/%s/manage_check_ins" % self.event.id)
        trs = response.soup.find("table").findAll("tr")
        self.assertEquals(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Check Out")

        self.assertIsNotNone(check_in_button)
        self.assertIsNone(check_out_button)

        response = self.client.get(check_in_button['href'], follow=True)
        # This should check them in then redirect back

        trs = response.soup.find("table").findAll("tr")
        self.assertEquals(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Cancel Check In")

        self.assertIsNone(check_in_button)
        self.assertIsNotNone(check_out_button)

        response = self.client.get(check_out_button['href'], follow=True)
        # This will check them out then redirect back

        trs = response.soup.find("table").findAll("tr")
        self.assertEquals(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Cancel Check In")

        self.assertIsNotNone(check_in_button)
        self.assertIsNone(check_out_button)
