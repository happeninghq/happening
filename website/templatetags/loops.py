""" Template tags relating to iteration and loops. """

from django import template

register = template.Library()


@register.filter(name='times1')
def times1(number):
    """ Return a range up to the given number, starting at 1, inclusive. """
    return range(1, number + 1)
