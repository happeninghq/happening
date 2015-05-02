"""Admin notifications."""
from happening.notifications import Notification


class AdminEventMessageNotification(Notification):

    """A message from administrators regarding an event."""

    required_data = ["message", "event_name"]
    optional_data = ["subject"]
    category = "Events"

    send_notification = False
    can_edit_send_notification = False


class AdminMessageNotification(Notification):

    """A message from administrators."""

    required_data = ["message"]
    optional_data = ["subject"]

    send_notification = False
    can_edit_send_notification = False
