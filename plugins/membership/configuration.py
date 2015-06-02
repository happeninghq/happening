"""Membership configuration."""
from happening import configuration
from happening import forms


class MembershipMessage(configuration.CharField):

    """The message shown on the page where membership can be taken out."""

    field = forms.EpicEditorField
    renderer = configuration.MarkdownRenderer()
