"""Event notifications."""
from happening.notifications import Notification


class EventInformationNotification(Notification):

    """An event you have tickets to is coming up."""

    required_data = ["event", "event_name", "time_to_event",
                     "is_final_notification", "is_voting"]
    category = "Events"


class CancelledTicketNotification(Notification):

    """You have cancelled your tickets for an event."""

    required_data = ["ticket", "event", "event_name"]
    category = "Events"


class EditedTicketNotification(Notification):

    """You have edited your tickets for an event."""

    required_data = ["ticket", "event", "event_name"]
    category = "Events"


class PurchasedTicketNotification(Notification):

    """You have purchased tickets for an event."""

    required_data = ["ticket", "event", "event_name"]
    category = "Events"
