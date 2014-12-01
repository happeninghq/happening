""" Test about page. """

from django_bs_test import TestCase


class TestAbout(TestCase):

    """ Test about page. """

    def test_about(self):
        """ Test it renders. """
        response = self.client.get("/about")
        self.assertEqual(200, response.status_code)
