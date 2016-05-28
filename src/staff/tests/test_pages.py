"""Test managing pages."""

from happening.tests import TestCase
from model_mommy import mommy
from django.conf import settings
from pages.models import Page


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

    def test_create_page(self):
        """Test creating pages."""
        self.client.login(username=self.user.username, password="password")

        response = self.client.get("/staff/pages/create")
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/staff/pages/create", {

        })

    def test_edit_page(self):
        """Test editing pages."""
        self.client.login(username=self.user.username, password="password")
        page = mommy.make("Page")
        response = self.client.get("/staff/pages")
        trs = response.soup.find("table").findAll("tr")
        edit_url = trs[1].find("a", "edit_page")['href']

        response = self.client.get(edit_url)

        self.assertEqual(
            response.soup.find("input", {"id": "id_url"})['value'].strip(),
            page.url)
        self.assertEqual(
            response.soup.find("input", {"id": "id_title"})['value'].strip(),
            page.title)
        self.assertEqual(
            response.soup.find("textarea", {"id": "id_content"}).text.strip(),
            page.content)

        response = self.client.post(
            edit_url,
            {
                "url": "test123",
                "title": "test title",
                "content": "test content"
            }, follow=True)

        page = Page.objects.get(pk=page.pk)

        self.assertEqual(page.url, "test123")
        self.assertEqual(page.title, "test title")
        self.assertEqual(page.content, "test content")

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
