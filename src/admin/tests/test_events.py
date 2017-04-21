"""Test administrating events."""

from happening.tests import TestCase
from model_mommy import mommy
from datetime import datetime, timedelta
from events.models import Event
import pytz
from uuid import uuid4
from django.core import mail
from django.conf import settings
from django.utils import timezone


class TestEvents(TestCase):

    """Test administrating events."""

    def setUp(self):
        """Set up a user."""
        super(TestEvents, self).setUp()
        self.user = self.create_admin()

        self.event = mommy.make("Event", start=datetime.now(pytz.utc) +
                                timedelta(days=2))
        # self.ticket_type = mommy.make("TicketType", event=self.event,
        #                               number=30, visible=True)

    def test_send_email(self):
        """Test that administrators can send emails to attending members."""
        test_subject = uuid4().hex
        test_content = uuid4().hex
        # With a single attendee
        user = mommy.make(settings.AUTH_USER_MODEL,
                          email="test@happeninghq.com")
        mommy.make("Ticket", event=self.event, user=user)
        self.client.login(username=self.user.username, password="password")

        self.client.post("/admin/events/%s/email" % self.event.id, {
            "to": "tickets__has:(event__id:%s cancelled:False)" %
            self.event.id,
            "subject": test_subject,
            "content": test_content,
            "start_sending": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stop_sending": (timezone.now() + timedelta(days=1))
            .strftime("%Y-%m-%d %H:%M:%S")
            })
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(test_subject, mail.outbox[0].subject)
        self.assertTrue(test_content in mail.outbox[0].body)
        mail.outbox = []

        # With two attendees
        user2 = mommy.make(settings.AUTH_USER_MODEL,
                           email="test2@happeninghq.com")
        mommy.make("Ticket", event=self.event, user=user2)
        self.client.post("/admin/events/%s/email" % self.event.id, {
            "to": "tickets__has:(event__id:%s cancelled:False)" %
            self.event.id,
            "subject": test_subject,
            "content": test_content,
            "start_sending": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stop_sending": (timezone.now() + timedelta(days=1))
            .strftime("%Y-%m-%d %H:%M:%S")
            })
        self.assertEqual(2, len(mail.outbox))

    def test_events(self):
        """Test listing events."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/admin/events")
        # We should have the title row and then 1 row for an event
        self.assertEqual(2, len(response.soup.find("table").findAll("tr")))
        for i in range(10):
            mommy.make("Event", start=datetime.now(pytz.utc) +
                       timedelta(days=i))

        response = self.client.get("/admin/events")
        # We only show up to 10 per page
        self.assertEqual(12, len(response.soup.find("table").findAll("tr")))

    def test_event(self):
        """Test viewing an event page."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/admin/events/%s" % self.event.id)

        # Check that no tickets are listed
        self.assertEqual(1, len(response.soup.find("table").findAll("tr")))

        mommy.make("Ticket", event=self.event, user=self.user)

        # Check it lists the ticket
        response = self.client.get("/admin/events/%s" % self.event.id)
        self.assertEqual(2, len(response.soup.find(
            "table", id="attendees-list").findAll("tr")))

    def test_edit_event(self):
        """Test editing events."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/admin/events/%s/edit" % self.event.id)

        # Check that information is being loaded into the form
        self.assertEqual(self.event.title, response.soup.find("input",
                         {"id": "id_title"})["value"])

        response = self.client.post("/admin/events/%s/edit" % self.event.id, {
            "title": "NEW TITLE",
            "start": "2010-05-05 19:00:00",
            "tickets": "[]"
        }, follow=True)
        self.assertTrue("/admin/events/%s" % self.event.id in
                        response.redirect_chain[0][0])

        self.event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(self.event.title, "NEW TITLE")

    def test_create_event(self):
        """Test creating events."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/admin/events/create")

        response = self.client.post("/admin/events/create", {
            "title": "NEW TITLE",
            "start": "2010-05-05 19:00:00",
            "tickets": "[]"
        }, follow=True)
        self.assertTrue("/admin/events" in
                        response.redirect_chain[0][0])

    def test_add_attendee(self):
        """Test adding an attendee after an event begins."""
        second_user = mommy.make(settings.AUTH_USER_MODEL)

        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/admin/events/%s" % self.event.id)

        self.assertIsNotNone(
            response.soup.find(
                "a",
                {"href": "/admin/events/%s/add_attendee" % self.event.id}))

        response = self.client.get(
            "/admin/events/%s/add_attendee" % self.event.id)

        trs = response.soup.find("table").findAll("tr")

        # This should list all users who haven't got tickets
        # For now AnonymousUser is included - TODO GET RID
        self.assertEqual(4, len(trs))

        # (Header + staff + not staff)

        response = self.client.post(
            "/admin/events/%s/add_attendee" % self.event.id,
            {
                "member_pk": self.user.pk
            }, follow=True)

        self.assertTrue("/admin/events/%s" % self.event.id in
                        response.redirect_chain[0][0])

        self.assertEqual(2, len(response.soup.find("table",
                         id="attendees-list").findAll("tr")))

        response = self.client.post(
            "/admin/events/%s/add_attendee" % self.event.id,
            {
                "member_pk": second_user.pk
            }, follow=True)

        self.assertTrue("/admin/events/%s" % self.event.id in
                        response.redirect_chain[0][0])

        self.assertEqual(3, len(response.soup.find("table",
                         id="attendees-list").findAll("tr")))

    def test_check_in(self):
        """Test checking in."""
        self.client.login(username=self.user.username, password="password")

        mommy.make("Ticket", event=self.event, user=self.user)

        # Check it lists the ticket
        response = self.client.get("/admin/events/%s" % self.event.id)
        trs = response.soup.find("table", id="attendees-list").findAll("tr")
        self.assertEqual(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Check Out")

        self.assertIsNotNone(check_in_button)
        self.assertIsNone(check_out_button)

        response = self.client.get(check_in_button['href'], follow=True)
        # This should check them in then redirect back

        trs = response.soup.find("table",
                                 id="attendees-list").findAll("tr")
        self.assertEqual(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Cancel Check In")

        self.assertIsNone(check_in_button)
        self.assertIsNotNone(check_out_button)

        response = self.client.get(check_out_button['href'], follow=True)
        # This will check them out then redirect back

        trs = response.soup.find("table", id="attendees-list").findAll("tr")
        self.assertEqual(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Cancel Check In")

        self.assertIsNotNone(check_in_button)
        self.assertIsNone(check_out_button)

    def test_manage_check_ins(self):
        """Test checking in using dedicated page."""
        self.client.login(username=self.user.username, password="password")

        mommy.make("Ticket", event=self.event, user=self.user)

        # Check it lists the ticket
        response = self.client.get(
            "/admin/events/%s/manage_check_ins" % self.event.id)
        trs = response.soup.find("table").findAll("tr")
        self.assertEqual(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Check Out")

        self.assertIsNotNone(check_in_button)
        self.assertIsNone(check_out_button)

        response = self.client.get(check_in_button['href'], follow=True)
        # This should check them in then redirect back

        trs = response.soup.find("table").findAll("tr")
        self.assertEqual(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Cancel Check In")

        self.assertIsNone(check_in_button)
        self.assertIsNotNone(check_out_button)

        response = self.client.get(check_out_button['href'], follow=True)
        # This will check them out then redirect back

        trs = response.soup.find("table").findAll("tr")
        self.assertEqual(2, len(trs))

        check_in_button = trs[1].find("a", text="Check In")
        check_out_button = trs[1].find("a", text="Cancel Check In")

        self.assertIsNotNone(check_in_button)
        self.assertIsNone(check_out_button)
