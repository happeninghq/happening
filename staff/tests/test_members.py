"""Test managing members."""

from happening.tests import TestCase
from model_mommy import mommy
from django.conf import settings


class TestStaffMembers(TestCase):

    """Test managing members."""

    def setUp(self):
        """Set up user."""
        self.user = mommy.make(settings.AUTH_USER_MODEL, is_staff=True)
        self.user.set_password("password")
        self.user.save()

    def test_list_members(self):
        """Test we can list members."""
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/staff/members")
        self.assertEquals(response.status_code, 200)

        trs = response.soup.find("table").findAll("tr")
        self.assertEquals(2, len(trs))
        self.assertEquals(self.user.username, trs[1].find("td").text)

        for i in range(10):
            mommy.make(settings.AUTH_USER_MODEL)

        response = self.client.get("/staff/members")
        self.assertEquals(12, len(response.soup.find("table").findAll("tr")))
