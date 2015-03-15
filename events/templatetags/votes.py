"""Template tags relating to voting."""

from django import template

register = template.Library()


@register.filter(name="languages_for_event")
def languages_for_event(event, user):
    """Return a list of languages voted for by this user."""
    ticket = event.tickets.get(user=user, cancelled=False)
    if not ticket:
        return []
    return ticket.default_votes


@register.filter(name='user_has_voted')
def user_has_voted(event, user):
    """Return True if the user has voted on this event."""
    ticket = event.tickets.get(user=user, cancelled=False)
    if not ticket:
        return False
    return ticket.votes is not None
