"""Group tags."""
from django import template
from plugins.groups.event_configuration import GroupCreation
from events.templatetags.tickets import user_has_tickets

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


@register.filter
def can_create_group(user, event):
    """Can the user create a group for the given event."""
    if not user_has_tickets(user, event):
        return False
    if has_group(user, event):
        return False  # Can't be in two groups
    g = GroupCreation(event).get()
    if g == "0":
        print "NOO"
        # Never
        return False
    elif g == "2":
        print "TRUU"
        # Any time
        return True
    else:
        print "ANOO"
        # After it has started
        return not event.is_future