"""Membership models."""
from happening import db
from django.conf import settings
from django.db import models
from django.utils import timezone
from members.models import Profile


class Membership(db.Model):

    """A payment made to upgrade membership."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="memberships")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    amount = models.IntegerField()
    payment_id = models.CharField(max_length=200)

    @property
    def is_active(self):
        """True if the membership is still active."""
        return self.end_time > timezone.now()


def active_paid_membership(self):
        """Return most recent active membership, None if there is none."""
        return self.user.memberships.filter(
            end_time__gt=timezone.now()).order_by("start_time").first()

Profile.active_paid_membership = active_paid_membership
