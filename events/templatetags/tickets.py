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
def active_tickets_json(event, user=None):
    """Return json of available tickets for ticket widget."""
    def ticket_type_to_dict(ticket_type, purchasable):
        ret = {
            "name": ticket_type.name,
            "remaining_tickets": ticket_type.remaining_tickets,
            "price": ticket_type.price,
            "pk": ticket_type.pk}
        if not purchasable:
            ret["remaining_tickets"] = 0
        return ret

    return json.dumps([ticket_type_to_dict(t, t.purchasable_by(user)) for t in
                       event.ticket_types.active()])


@register.filter()
def purchasable_by(ticket_type, user):
    """The ticket is/not purchasable by the user."""
    return ticket_type.purchasable_by(user)
