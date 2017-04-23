"""Test GAnalytics."""

from happening.tests import TestCase
from uuid import uuid4
from pages.configuration import GoogleAnalyticsCode


class TestGAnalytics(TestCase):

    """Test Google Analytics."""

    def test_ganalytics(self):
        """Test that google analytics is injected."""

        uuid = uuid4().hex

        response = self.client.get("/accounts/login/")
        self.assertTrue(uuid not in str(response.soup))

        c = GoogleAnalyticsCode()
        c.set_enabled(True)
        c.set(uuid)

        response = self.client.get("/accounts/login/")
        self.assertTrue(uuid in str(response.soup))
