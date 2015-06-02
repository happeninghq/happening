"""Payment models."""
from django.db import models
from happening import db
from django_pgjson.fields import JsonField
from django.contrib.auth.models import User
from datetime import datetime


class Payment(db.Model):

    """Represents a payment which may or may not be paid yet."""

    # Payments must be made by a user
    user = models.ForeignKey(User)

    # Shown on the bank statement
    description = models.TextField()

    created_datetime = models.DateTimeField(auto_now_add=True)

    # The amount in pennies
    amount = models.IntegerField()

    success_url_name = models.CharField(max_length=255)
    failure_url_name = models.CharField(max_length=255)

    # This is passed to the payment processor
    metadata = JsonField(default={})

    # This is instead of using _data which may be used to pass data
    # to the success/failure views
    extra = JsonField(default={})

    # Should be PENDING, PAID, or FAILED
    _status = models.CharField(max_length=7, default="PENDING")
    status_changed_datetime = models.DateTimeField(null=True)

    # This is used to mark a payment as "complete" so that people don't
    # for example, issue two products just by refreshing the "complete" view
    _complete = models.BooleanField(default=False)
    complete_datetime = models.DateTimeField(null=True)

    error = models.TextField(null=True)
    reciept_id = models.TextField(null=True)

    @property
    def complete(self):
        """The payment complete or not."""
        return self._complete

    @complete.setter
    def complete(self, val):
        """Set the payment as complete."""
        if not val == self._complete:
            self._complete = val
            self.complete_datetime = datetime.now()
            self.save()

    @property
    def status(self):
        """The status of the payment."""
        return self._status

    @status.setter
    def status(self, val):
        """Change status."""
        if val not in ["PENDING", "PAID", "FAILED"]:
            raise ValueError("Must be PENDING, PAID, or FAILED")
        if not val == self._status:
            self._status = val
            self.status_changed_datetime = datetime.now()
            self.save()


class PaymentManager(models.Manager):

    """Custom PaymentHandler Manager, to get active handler."""

    def active(self):
        """Get the active handler (if any)."""
        return self.filter(active=True).first()


class PaymentHandler(db.Model):

    """Represent a Stripe instance configured to accept payment.

    We currently only accept Stripe but will accept more in future.
    """

    objects = PaymentManager()

    description = models.CharField(max_length=255)

    public_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)

    active = models.BooleanField(default=False)
