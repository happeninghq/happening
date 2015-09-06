"""Test administrating event presets."""

from happening.tests import TestCase
from model_mommy import mommy
from events.models import EventPreset
from django.conf import settings
import json


class TestEventPresets(TestCase):

    """Test administrating event presets."""

    def setUp(self):
        """Set up a user."""
        super(TestEventPresets, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL, is_staff=True)
        self.user.set_password("password")
        self.user.save()

    def test_event_presets(self):
        """Test listing event presets."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/staff/event_presets")

        self.assertIsNone(response.soup.find("table"))
        for i in range(10):
            mommy.make("EventPreset")

        response = self.client.get("/staff/event_presets")

        self.assertEquals(11, len(response.soup.find("table").findAll("tr")))

    def test_edit_event_preset(self):
        """Test editing event presets."""
        self.client.login(username=self.user.username, password="password")

        event_preset = mommy.make("EventPreset", value=json.dumps(
            {"title": "test title"}
        ))

        response = self.client.get(
            "/staff/event_presets/%s/edit" % event_preset.id)

        # Check that information is being loaded into the form
        self.assertEquals("test title", response.soup.find("input",
                          {"id": "id_title"})["value"])

        response = self.client.post(
            "/staff/event_presets/%s/edit" % event_preset.id, {
                "title": "NEW TITLE",
                "datetime": "2010-05-05 19:00:00"
            }, follow=True)

        event_preset = EventPreset.objects.get(pk=event_preset.pk)
        self.assertEquals(json.loads(event_preset.value)["title"], "NEW TITLE")

    def test_create_event_preset(self):
        """Test creating event presets."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/staff/event_presets/create")

        response = self.client.post("/staff/event_presets/create", {
            "title": "NEW TITLE",
            "datetime": "2010-05-05 19:00:00"
        }, follow=True)

        self.assertTrue("/staff/event_presets" in
                        response.redirect_chain[0][0])

        event_preset = EventPreset.objects.get(pk=1)
        self.assertEquals(json.loads(event_preset.value)["title"], "NEW TITLE")

    def test_delete_event_preset(self):
        """Test deleting event presets."""
        self.client.login(username=self.user.username, password="password")

        event_preset = mommy.make("EventPreset")
        response = self.client.get("/staff/event_presets")

        self.assertEquals(2, len(response.soup.find("table").findAll("tr")))

        self.client.post("/staff/event_presets/%s/delete" % event_preset.id)

        response = self.client.get("/staff/event_presets")
        self.assertIsNone(response.soup.find("table"))
