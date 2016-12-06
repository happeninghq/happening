"""Test notify."""

from happening.tests import TestCase
from model_mommy import mommy
from django.conf import settings
from happening.notifications import notify_following
from happening.notifications import notify_admins
from events.notifications import CancelledTicketNotification
from notifications.models import Notification


class TestNotify(TestCase):

    """Test notify."""

    def setUp(self):
        """Set up users."""
        super(TestNotify, self).setUp()
        self.users = [mommy.make(settings.AUTH_USER_MODEL) for x in range(5)]
        self.staff = [mommy.make(settings.AUTH_USER_MODEL,
                                 is_staff=True) for x in range(5)]
        self.admins = [mommy.make(settings.AUTH_USER_MODEL,
                                  is_staff=True,
                                  is_superuser=True) for x in range(5)]

    def test_notify_following(self):
        """Test we can notify followers."""
        # We'll use users[0] as the "followed"

        self.users[1].follow(self.users[0], "test")
        self.users[2].follow(self.users[0], "test")
        self.users[3].follow(self.users[0], "test")

        notify_following(self.users[0], "test", CancelledTicketNotification,
                         {"ticket": "test", "event": {"id": "1"},
                          "event_name": "test"},
                         ignore=[self.users[1]])

        for user in self.staff + self.admins + [self.users[0],
                                                self.users[1],
                                                self.users[4]]:
            self.assertEquals(Notification.objects.get_for_user(
                user).count(), 0)
        self.assertEquals(Notification.objects.get_for_user(
            self.users[2]).count(), 1)
        self.assertEquals(Notification.objects.get_for_user(
            self.users[3]).count(), 1)

    def test_notify_admins(self):
        """Test we can notify admins."""
        notify_admins(CancelledTicketNotification,
                      {"ticket": "test", "event": {"id": "1"},
                       "event_name": "test"},
                      ignore=[self.admins[0]])

        for user in self.users + self.staff + [self.admins[0]]:
            self.assertEquals(Notification.objects.get_for_user(
                user).count(), 0)
        for user in self.admins[1:]:
            self.assertEquals(Notification.objects.get_for_user(
                user).count(), 1)
