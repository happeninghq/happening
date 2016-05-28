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


class CanPurchaseFromWaitingListNotification(Notification):

    """You are now able to purchase a ticket from the waiting list."""

    required_data = ["event", "event_name", "timeout"]
    category = "Events"


class WaitingListExpiredNotification(Notification):

    """You have been removed from the waiting list due to the time limit."""

    required_data = ["event", "event_name"]
    category = "Events"
