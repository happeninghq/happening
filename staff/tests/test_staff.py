"""Test sending emails."""

from happening.tests import TestCase
from model_mommy import mommy
from django.conf import settings


class TestStaff(TestCase):
    """Test staff views."""

    def setUp(self):
        """Set up users."""
        super(TestStaff, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL, is_staff=True)
        self.user.set_password("password")
        self.user.save()

        self.non_staff_user = mommy.make(settings.AUTH_USER_MODEL)
        self.non_staff_user.set_password("password")
        self.non_staff_user.save()

    def test_dashboard(self):
        """Test dashboard loads only for staff."""
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/staff/")
        self.assertEquals(response.status_code, 200)

        self.client.login(username=self.non_staff_user.username,
                          password="password")
        response = self.client.get("/staff/")
        self.assertEquals(response.status_code, 302)
