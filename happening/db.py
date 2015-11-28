"""Happening database functionality."""
from django.db import models
from django_pgjson.fields import JsonField


class Model(models.Model):

    """All happening Models should subclass this."""

    _data = JsonField(default={})

    class Meta:
        abstract = True


class AddressField(JsonField):

    """Field for storing address information."""

    def formfield(self, **kwargs):
        """Load correct form field for address."""
        from happening import forms
        return forms.AddressField(**kwargs)
