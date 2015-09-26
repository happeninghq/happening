"""Event Configuration."""
from happening import configuration


class TicketTimeout(configuration.IntegerField):

    """How long (seconds) do people have to pay during purchase."""

    default = 600
