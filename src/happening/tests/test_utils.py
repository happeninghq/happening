"""Test utils."""

from happening.tests import TestCase
from happening.utils import externalise_url, externalise_urls


class TestUtils(TestCase):

    """Test utils."""

    def test_externalise_url(self):
        """Test we can externalise a single url."""
        self.assertEqual(externalise_url("a/b"), "http://example.com/a/b")

    def test_externalise_urls(self):
        """Test we can externalise markdown urls in a string."""
        self.assertEqual(
            externalise_urls("[a](a/b) [b](a/b)"),
            "[a](http://example.com/a/b) [b](http://example.com/a/b)")

    def test_externalise_urls_a_tag(self):
        """Test we can externalise <a> urls in a string."""
        self.assertEqual(
            externalise_urls("<a href=\"a/b\">a</a> <a href=\"a/b\">b</a>"),
            "<a href=\"http://example.com/a/b\">a</a> " +
            "<a href=\"http://example.com/a/b\">b</a>")
