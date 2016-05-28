"""Template tags relating to types."""

from django import template

register = template.Library()


@register.filter()
def is_dict(t):
    """True if this a dict."""
    return isinstance(t, dict)
