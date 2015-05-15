"""Event Configuration."""
from happening import configuration
from happening import forms


class Description(configuration.CharField):

    """Event Description."""

    field = forms.EpicEditorField
    renderer = configuration.MarkdownRenderer()


class TicketPurchasedMessage(configuration.CharField):

    """Message to show when a ticket is purchased."""

    field = forms.EpicEditorField
    renderer = configuration.MarkdownRenderer()
