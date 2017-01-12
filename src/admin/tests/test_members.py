"""Test managing members."""

from happening.tests import TestCase
from model_mommy import mommy
from django.conf import settings


class TestStaffMembers(TestCase):

    """Test managing members."""

    def setUp(self):
        """Set up user."""
        super(TestStaffMembers, self).setUp()
        self.user = self.create_admin()

    def test_list_members(self):
        """Test we can list members."""
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/admin/members")
        self.assertEqual(response.status_code, 200)

        trs = response.soup.find("table").findAll("tr")
        # TMP includes AnonymousUser TODO: Deal with this
        self.assertEqual(3, len(trs))
        self.assertEqual(self.user.username, trs[2].find("td").text)

        for i in range(10):
            mommy.make(settings.AUTH_USER_MODEL)

        response = self.client.get("/admin/members")
        self.assertEqual(13, len(response.soup.find("table").findAll("tr")))
