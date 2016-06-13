"""Event Configuration."""
from happening import configuration
from datetime import timedelta


class TicketTimeout(configuration.DurationField):

    """How long do people have to pay during purchase."""

    default = timedelta(minutes=10)
    category = "Tickets"


class WaitingListTimeout(configuration.DurationField):

    """How long do people have to purchase from a waiting list."""

    default = timedelta(days=1)
    category = "Tickets"
