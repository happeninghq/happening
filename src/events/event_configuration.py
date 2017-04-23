"""Event Configuration."""
from happening import configuration
from happening import forms


class Description(configuration.CharField):

    """Event Description."""

    field = forms.MarkdownField
    renderer = configuration.MarkdownRenderer()


class MaxTicketsPerPerson(configuration.IntegerField):

    """Should the total number of tickets per person be limited."""

    can_be_disabled = True
    default_enabled = False

    default = 1


class RSVPInformation(configuration.CharField):

    """Information shown to people who have RSVPd.
       This should include e.g. ticket information."""

    field = forms.MarkdownField
    renderer = configuration.MarkdownRenderer()

    can_be_disabled = True
    default_enabled = False
