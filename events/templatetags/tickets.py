"""Template tags relating to tickets."""

from django import template
import json

register = template.Library()


@register.filter()
def has_tickets(user, event):
    """Return True if the user has tickets for this event."""
    if user.is_authenticated():
        return event.tickets.filter(user=user, cancelled=False).count() > 0
    return False


@register.filter()
def tickets(user, event):
    """Return the tickets the user has for the event."""
    if user.is_authenticated():
        return event.tickets.filter(user=user, cancelled=False)
    return []


@register.filter()
def orders(user, event):
    """Return the orders the user has for the event."""
    if user.is_authenticated():
        return [o for o in event.orders.filter(user=user) if not o.cancelled]
    return []


@register.filter()
def other_tickets(user, event):
    """Return the tickets the user has for the event that have no order."""
    # All of this functionality is legacy and will be removed
    if user.is_authenticated():
        return event.tickets.filter(user=user, cancelled=False, order=None)
    return []


@register.filter()
def purchasable_tickets_json(event):
    """Return json of available tickets for ticket widget."""
    def ticket_type_to_dict(ticket_type):
        return {
            "name": ticket_type.name,
            "remaining_tickets": ticket_type.remaining_tickets,
            "price": ticket_type.price,
            "pk": ticket_type.pk}

    return json.dumps([ticket_type_to_dict(t) for t in
                       event.ticket_types.purchasable()])
