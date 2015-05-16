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
        # We only show up to 10 per page
        self.assertEquals(11, len(response.soup.find("table").findAll("tr")))
        response = self.client.get("/staff/members?page=2")
        # Final one on the next page
        self.assertEquals(2, len(response.soup.find("table").findAll("tr")))

    def test_make_staff(self):
        """Test we can make a member staff."""
        self.client.login(username=self.user.username, password="password")
        mommy.make(settings.AUTH_USER_MODEL)

        response = self.client.get("/staff/members")
        trs = response.soup.find("table").findAll("tr")
        # [1] is ourself, so we can't toggle staff
        staff_td = trs[1].find("td", "is_staff")
        self.assertEquals("True", staff_td.text.strip())
        self.assertIsNone(staff_td.find("a"))

        # [1] is another user
        staff_td = trs[2].find("td", "is_staff")
        self.assertEquals("False", staff_td.text.strip())
        self.assertIsNotNone(staff_td.find("a"))

        response = self.client.post(staff_td.find("a")['href'], follow=True)
        trs = response.soup.find("table").findAll("tr")
        # Will set to staff and redirect to current page

        # [1] is another user
        staff_td = trs[2].find("td", "is_staff")
        self.assertEquals("True", staff_td.text.strip())
        self.assertIsNotNone(staff_td.find("a"))

        response = self.client.post(staff_td.find("a")['href'], follow=True)
        trs = response.soup.find("table").findAll("tr")
        # Will set to not staff and redirect to current page

        # [1] is another user
        staff_td = trs[2].find("td", "is_staff")
        self.assertEquals("False", staff_td.text.strip())
        self.assertIsNotNone(staff_td.find("a"))
