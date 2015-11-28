"""Event Configuration."""
from happening import configuration
from happening import forms


class Description(configuration.CharField):
    """Event Description."""

    field = forms.MarkdownField
    renderer = configuration.MarkdownRenderer()


class MaxTicketsPerPerson(configuration.IntegerField):
    """Do we limit the total number of tickets per person."""

    can_be_disabled = True
    default_enabled = False

    default = 1
