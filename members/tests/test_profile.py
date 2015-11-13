"""Test viewing and editing profile."""

from happening.tests import TestCase
from model_mommy import mommy
from django.contrib.auth import get_user_model
from django.conf import settings


class TestProfile(TestCase):
    """Test viewing and editing profile."""

    def setUp(self):
        """Set up a user."""
        super(TestProfile, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL)
        self.user.set_password("password")
        self.user.save()

    def test_nonexisting_user_404s(self):
        """Test that a nonexisting profile returns a 404."""
        response = self.client.get("/member/999", follow=True)
        self.assertEquals(404, response.status_code)

    def test_can_view_profile(self):
        """Test that we can view an existing profile."""
        response = self.client.get("/member/%s" % self.user.id)
        self.assertTrue(str(self.user.profile) in response.content)
        self.assertTrue(str(self.user.profile.bio) in response.content)

    def test_cannot_edit_other_profiles(self):
        """Test that users cannot edit other people's profiles."""
        user2 = mommy.make(settings.AUTH_USER_MODEL)
        user2.set_password("password")
        user2.save()

        # First check logged out user can't edit profiles
        for url in ["/member/%s/edit"]:
            response = self.client.get(url % self.user.id, follow=True)
            self.assertTrue("accounts/login" in response.redirect_chain[0][0])

        # Then check that logged in users can't edit other user's profiles
        self.client.login(username=user2.username, password="password")
        for url in ["/member/%s/edit"]:
            response = self.client.get(url % self.user.id)
            self.assertEquals(404, response.status_code)

    def test_can_edit_profile_fields(self):
        """Test a user can edit their own text profile fields."""
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/member/%s/edit" % self.user.id)
        self.assertEquals(200, response.status_code)

        response = self.client.post("/member/%s/edit" % self.user.id,
                                    {"first_name": "j",
                                     "last_name": "s",
                                     "bio": "test 1 2 3"}, follow=True)
        self.assertTrue(
            "/member/%s" % self.user.id in response.redirect_chain[0][0])

        self.user = get_user_model().objects.get(pk=self.user.id)
        self.assertEquals("j", self.user.first_name)
        self.assertEquals("s", self.user.last_name)
        self.assertEquals("test 1 2 3", self.user.profile.bio)

    def test_default_photo(self):
        """Test that default photos are correct."""
        self.assertTrue("gravatar" in self.user.profile.photo_url())
