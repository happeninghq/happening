"""Payment models."""
from django.db import models
from happening import db
from django_pgjson.fields import JsonField
from django.contrib.auth.models import User


class Payment(db.Model):

    """Represents a payment which may or may not be paid yet."""

    # Payments must be made by a user
    user = models.ForeignKey(User)

    # Shown on the bank statement
    description = models.TextField()

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
    # TODO: Restrict it
    status = models.CharField(max_length=7, default="PENDING")

    # This is used to mark a payment as "complete" so that people don't
    # for example, issue two products just by refreshing the "complete" view
    complete = models.BooleanField(default=False)

    error = models.TextField(null=True)
    reciept_id = models.TextField(null=True)


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
