"""Event Configuration."""
from happening import configuration
from happening import forms


class Description(configuration.CharField):
    """Event Description."""

    field = forms.MarkdownField
    renderer = configuration.MarkdownRenderer()


class MaxTicketsPerPerson(configuration.IntegerField):
    """0 Means unlimited."""

    default = 0
