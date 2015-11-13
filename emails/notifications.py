"""Event notifications."""
from happening.notifications import Notification


class EmailNotification(Notification):
    """An email has been sent."""

    required_data = ["subject", "content"]

    send_notification = False
