"""Template tags relating to waiting lists."""

from django import template

register = template.Library()


@register.filter
def waiting_list_contains(ticket_type, user):
    """Return True if the user is on the waiting list for this ticket."""
    return ticket_type.waiting_list_contains(user)
