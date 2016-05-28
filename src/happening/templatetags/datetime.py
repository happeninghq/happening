"""Time template tags."""
from time import mktime

from django import template

register = template.Library()


@register.filter
def epoch(value):
    """Convert a datetime into a timestamp."""
    try:
        return int(mktime(value.timetuple())*1000)
    except:
        return None
