"""Event notifications."""
from happening.notifications import Notification


class CancelledTicketNotification(Notification):
    """You have cancelled your tickets for an event."""

    required_data = ["ticket", "event", "event_name"]
    category = "Events"


class PurchasedTicketNotification(Notification):
    """You have purchased tickets for an event."""

    required_data = ["order", "tickets_count", "event", "event_name"]
    category = "Events"
