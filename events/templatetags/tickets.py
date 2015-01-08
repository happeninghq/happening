""" Template tags relating to tickets. """

from django import template

register = template.Library()


@register.filter(name='has_tickets')
def user_has_tickets(user, event):
    """ Return True if the user has tickets for this event. """
    return event.votes.filter(user=user).count() > 0
