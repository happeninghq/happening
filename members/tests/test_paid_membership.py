""" Test paying for membership. """

from website.tests import TestCase
from model_mommy import mommy
from django.contrib.auth.models import User


class TestPaidMembership(TestCase):

    """ Test paying for membership. """

    def setUp(self):
        """ Set up a user. """
        self.user = mommy.make("auth.User")
        self.user.set_password("password")
        self.user.save()

    def test_shows_no_membership(self):
        pass

    def test_can_purchase_from_select(self):
        pass

    def test_other_value_works(self):
        pass

    def test_shows_memberships(self):
        pass