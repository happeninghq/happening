"""Template tags relating to iteration and loops."""

from django import template

register = template.Library()


@register.filter()
def times0(number):
    """Return a range up to the given number, starting at 0, inclusive."""
    return list(range(0, number + 1))


@register.filter()
def times1(number):
    """Return a range up to the given number, starting at 1, inclusive."""
    return list(range(1, number + 1))
