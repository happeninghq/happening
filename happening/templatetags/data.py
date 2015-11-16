"""Template tags relating to data."""

from django import template

register = template.Library()


@register.filter()
def data(obj, var=None):
    """Get the data dictionary from an object."""
    if var:
        return obj._data.get(var)
    return obj._data
