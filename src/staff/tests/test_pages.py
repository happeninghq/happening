"""Test managing pages."""

from happening.tests import TestCase
from model_mommy import mommy
from django.conf import settings


class TestPages(TestCase):

    """Test managing pages."""

    def setUp(self):
        """Set up user."""
        super(TestPages, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL, is_staff=True)
        self.user.set_password("password")
        self.user.save()

    def test_pages(self):
        """Test listing pages."""
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/staff/pages")

        # No pages, just header
        self.assertIsNone(response.soup.find("table"))

        mommy.make("Page")

        response = self.client.get("/staff/pages")
        self.assertIsNotNone(response.soup.find("table"))
        self.assertEqual(2, len(response.soup.find("table").findAll("tr")))

    # TODO: Test create page

    # TODO: Test edit page

    def test_delete_page(self):
        """Test deleting pages."""
        self.client.login(username=self.user.username, password="password")
        mommy.make("Page")
        response = self.client.get("/staff/pages")
        trs = response.soup.find("table").findAll("tr")
        delete_url = trs[1].find("a", "delete_page")['href']

        response = self.client.post(delete_url, follow=True)
        # Will delete and return to page
        self.assertIsNone(response.soup.find("table"))
