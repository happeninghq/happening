"""Happening database functionality."""
from django.db import models
from django_pgjson.fields import JsonField


class Model(models.Model):

    """All happening Models should subclass this."""

    _data = JsonField(default={})

    class Meta:
        abstract = True
