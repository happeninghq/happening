""" Template tags relating to strings. """

from django import template
from website.utils import convert_to_spaces

register = template.Library()


@register.filter()
def spaces(text):
    """ Convert CamelCase into Space Separated. """
    return convert_to_spaces(text)
