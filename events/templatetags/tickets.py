"""Template tags relating to tickets."""

from django import template

register = template.Library()


@register.filter(name='has_tickets')
def user_has_tickets(user, event):
    """Return True if the user has tickets for this event."""
    if user.is_authenticated():
        return event.tickets.filter(user=user, cancelled=False).count() > 0
    return False


@register.filter(name='tickets')
def user_tickets(user, event):
    """Return the tickets the user has for the event."""
    if user.is_authenticated():
        return event.tickets.filter(user=user, cancelled=False)
    return []


@register.filter(name='orders')
def user_orders(user, event):
    """Return the orders the user has for the event."""
    if user.is_authenticated():
        return [o for o in event.orders.filter(user=user) if not o.cancelled]
    return []


@register.filter(name='other_tickets')
def user_other_tickets(user, event):
    """Return the tickets the user has for the event that have no order."""
    # All of this functionality is legacy and will be removed
    if user.is_authenticated():
        return event.tickets.filter(user=user, cancelled=False, order=None)
    return []
