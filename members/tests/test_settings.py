"""Test viewing and editing settings."""

from happening.tests import TestCase
from model_mommy import mommy
from django.contrib.auth import get_user_model
from django.conf import settings


class TestSettings(TestCase):
    """Test viewing and editing settings."""

    def setUp(self):
        """Set up a user."""
        super(TestSettings, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL)
        self.user.set_password("password")
        self.user.save()

    def test_nonexisting_user_404s(self):
        """Test that a nonexisting settings returns a 404."""
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/member/999/settings", follow=True)
        self.assertEquals(404, response.status_code)

    def test_can_view_own_settings(self):
        """Test that we can view our own settings."""
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/member/%s/settings" % self.user.id)
        self.assertTrue("Settings" in response.content)

    def test_cannot_view_other_settings(self):
        """Test that users cannot view other people's settings."""
        user2 = mommy.make(settings.AUTH_USER_MODEL)
        user2.set_password("password")
        user2.save()

        # First check logged out user can't view settings
        for url in ["/member/%s/settings", "/member/%s/settings/username"]:
            response = self.client.get(url % self.user.id, follow=True)
            self.assertTrue("accounts/login" in response.redirect_chain[0][0])

        # Then check that logged in users can't view other user's settings
        self.client.login(username=user2.username, password="password")
        for url in ["/member/%s/settings", "/member/%s/settings/username"]:
            response = self.client.get(url % self.user.id)
            self.assertEquals(404, response.status_code)

    def test_can_edit_username(self):
        """Test a user can edit their own username."""
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            "/member/%s/settings/username" % self.user.id)
        self.assertEquals(200, response.status_code)

        response = self.client.post(
            "/member/%s/settings/username" % self.user.id,
            {"username": "test_new_username"}, follow=True)
        self.assertTrue(
            "/member/%s/settings" % self.user.id in
            response.redirect_chain[0][0])

        self.user = get_user_model().objects.get(pk=self.user.id)
        self.assertEquals("test_new_username", self.user.username)

        user2 = mommy.make(settings.AUTH_USER_MODEL)
        user2.set_password("password")
        user2.save()

        response = self.client.post(
            "/member/%s/settings/username" % self.user.id,
            {"username": user2.username}, follow=True)
        self.assertTrue("username must be unique" in response.content)

        self.assertEquals("test_new_username", self.user.username)
