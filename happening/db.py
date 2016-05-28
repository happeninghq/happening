"""Happening database functionality."""
from django.db import models
from django_pgjson.fields import JsonField


class Manager(models.Manager):

    """All managers should subclass this."""

    def get_for_user(self, user):
        """Get the objects the given user can see."""
        # TODO: Should be empty by default?
        return self.all()


class Model(models.Model):

    """All happening Models should subclass this."""

    _data = JsonField(default={})

    class Meta:
        abstract = True

    @staticmethod
    def has_read_permission(request):
        """Nobody can read."""
        return False

    def has_object_read_permission(self, request):
        """Nobody can read object."""
        return False

    @staticmethod
    def has_write_permission(request):
        """Nobody can write."""
        return False

    @staticmethod
    def has_create_permission(request):
        """Nobody can create."""
        return False


class AddressField(JsonField):

    """Field for storing address information."""

    def formfield(self, **kwargs):
        """Load correct form field for address."""
        from happening import forms
        return forms.AddressField(**kwargs)
