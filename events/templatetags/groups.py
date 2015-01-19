""" Template tags relating to groups. """

from django import template

register = template.Library()


@register.filter(name='has_info_for_group')
def has_info_for_group(event, group_number):
    """ Return True if the event has information for the given group. """
    return event.solutions.filter(team_number=group_number).count() > 0
