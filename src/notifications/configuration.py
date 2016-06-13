"""Notifications configuration."""
from happening import configuration
from happening import forms


class NotificationsEmailAddress(configuration.EmailField):

    """The email address to send notification emails from."""

    default = "noreply@happening.com"
    category = "Emails"


class EmailHeader(configuration.CharField):

    """The text at the beginning of an email."""

    default = "Hello **{{user}}**"
    field = forms.MarkdownField
    category = "Emails"


class EmailFooter(configuration.CharField):

    """The text at the end of an email."""

    default = "Thanks\nAdmin"
    field = forms.MarkdownField
    category = "Emails"
