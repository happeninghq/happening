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
def visible_tickets_json(event, user):
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
                       event.ticket_types.visible_to(user)])


@register.filter()
def purchasable_by(ticket_type, user):
    """The ticket is/not purchasable by the user."""
    return ticket_type.purchasable_by(user)


@register.filter()
def purchasable_tickets_no(event, user):
    """Return the number of tickets purchasable by a user for an event."""
    return sum([t.remaining_tickets for t in
                event.ticket_types.purchasable_by(user)])


@register.filter()
def waiting_list_available(event, user):
    """Return if waiting lists are available for this user."""
    return len([t for t in event.ticket_types.waiting_list_available()
                if t.visible_to(user)]) > 0


@register.filter()
def rsvp_going(user, event):
    """Return True if the user has indicated they will attend this event."""
    if user.is_authenticated():
        return user.rsvps.filter(event=event, going=True).count() > 0
    return False
