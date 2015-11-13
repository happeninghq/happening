"""Event Configuration."""
from happening import configuration
from happening import forms


class Description(configuration.CharField):
    """Event Description."""

    field = forms.MarkdownField
    renderer = configuration.MarkdownRenderer()
