"""Test basic layout."""

from happening.tests import TestCase
from model_mommy import mommy
from django.conf import settings


class TestLayout(TestCase):

    """Test basic layout."""

    def test_shows_login_link(self):
        """Test it shows a login link if the user is logged out."""
        response = self.client.get("/")
        self.assertIsNotNone(
            response.soup.find("a", {"href": "/accounts/login/"}))
        self.assertIsNone(
            response.soup.find("a", {"href": "/accounts/logout/"}))

    def test_shows_logged_in_links(self):
        """Test it has appropriate links for logged in users."""
        user = mommy.make(settings.AUTH_USER_MODEL)
        user.set_password("password")
        user.save()

        self.client.login(username=user.username, password="password")

        response = self.client.get("/")
        self.assertIsNone(
            response.soup.find("a", {"href": "/accounts/login/"}))
        self.assertIsNotNone(
            response.soup.find("a", {"href": "/accounts/logout/"}))
