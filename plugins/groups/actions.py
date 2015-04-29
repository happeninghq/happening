"""Group events."""
from happening.plugins import action


@action("events.ticket_cancelled")
def ticket_cancelled(ticket):
    """If a ticket is cancelled, ensure that it is not in any groups."""
    for g in ticket.groups.all():
        g.delete()
