"""Group tags."""
from django import template
from plugins.groups.event_configuration import GroupCreation, GroupEditing
from plugins.groups.event_configuration import GroupMovement
from events.templatetags.tickets import has_tickets

register = template.Library()


@register.filter
def can_edit_group(user, group):
    """Can the given user edit the given group."""
    return can_edit_groups(user, group.event) and group.is_editable_by(user)


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


@register.filter
def can_create_group(user, event):
    """Can the user create a group for the given event."""
    if not has_tickets(user, event):
        return False
    if has_group(user, event):
        return False  # Can't be in two groups
    g = GroupCreation(event).get()
    if g == "0":
        # Never
        return False
    elif g == "2":
        # Any time
        return True
    elif g == "1":
        # After it has started
        return not event.is_future
    else:
        # If checked in
        ticket = user.tickets.filter(event=event, cancelled=False).first()
        return ticket.checked_in


@register.filter
def can_edit_groups(user, event):
    """Can the user edit groups for the given event."""
    if not has_tickets(user, event):
        return False
    g = GroupEditing(event).get()
    if g == "0":
        # Never
        return False
    elif g == "2":
        # Any time
        return True
    elif g == "1":
        # After it has started
        return not event.is_future
    else:
        # If checked in
        ticket = user.tickets.filter(event=event, cancelled=False).first()
        return ticket.checked_in


@register.filter
def can_move_groups(user, event):
    """Can the user move groups for the given event."""
    if not has_tickets(user, event):
        return False
    g = GroupMovement(event).get()
    if g == "0":
        # Never
        return False
    elif g == "2":
        # Any time
        return True
    elif g == "1":
        # After it has started
        return not event.is_future
    else:
        # If checked in
        ticket = user.tickets.filter(event=event, cancelled=False).first()
        return ticket.checked_in
