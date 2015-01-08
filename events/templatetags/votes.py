""" Template tags relating to voting. """

from django import template

register = template.Library()


@register.filter(name='user_has_voted')
def user_has_voted(event, user):
    """ Return True if the user has voted on this event. """
    return event.votes.filter(user=user).count() > 0


@register.filter(name='votes_for_language')
def votes_for_language(event, language):
    """ Return the number of votes for the given language & event. """
    return event.votes.filter(language=language).count()
