"""Group tags."""
from django import template

register = template.Library()


@register.filter
def can_edit_group(user, group):
    """Can the given user edit the given group."""
    return group.is_editable_by(user)


@register.filter
def has_group(user, event):
    """True if the user has a group for the given event."""
    ticket = user.tickets.filter(event=event, cancelled=False).first()
    if not ticket:
        return False
    return ticket.groups.count() > 0


@register.filter
def group(user, event):
    """The user's group for the given event."""
    ticket = user.tickets.filter(event=event, cancelled=False).first()
    if not ticket:
        return None
    group = ticket.groups.first()
    if not group:
        return None
    return group.group
