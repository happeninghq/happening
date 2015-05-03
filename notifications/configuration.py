"""Notifications configuration."""
from happening import configuration


class NotificationsEmailAddress(configuration.EmailField):

    """The email address to send notification emails from."""

    default = "noreply@happening.com"
