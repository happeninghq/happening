"""Finances models."""
from django.db import models
from happening import db
from payments.templatetags.currency import format_currency
from django.db.models import Sum


class Account(db.Model):

    """A financial account."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    @property
    def total(self):
        """Calculate the current total for the account."""
        s = self.transactions.aggregate(Sum('amount'))["amount__sum"]
        if not s:
            return 0
        return s

    def __unicode__(self):
        """Return the account name."""
        return self.name


class Category(db.Model):

    """A financial category."""

    name = models.CharField(max_length=255, unique=True)


class Payee(db.Model):

    """A financial payee."""

    name = models.CharField(max_length=255, unique=True)


class Transaction(db.Model):

    """A financial transaction."""

    account = models.ForeignKey(Account, related_name="transactions")
    date = models.DateField()
    category = models.ForeignKey(Category, related_name="transactions")
    payee = models.ForeignKey(Payee, related_name="transactions")
    memo = models.TextField(null=True)
    amount = models.IntegerField()  # Amount in pennies

    @property
    def inflow(self):
        """Format inflow value as a string."""
        if self.amount > 0:
            return format_currency(self.amount)
        return ""

    @property
    def outflow(self):
        """Format outflow value as a string."""
        if self.amount < 0:
            return format_currency(0 - self.amount)
        return ""
