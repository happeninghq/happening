"""Template tags relating to markdown."""

from django import template

register = template.Library()


@register.filter()
def blockquote(text):
    """Add > at the beginning of each line (a markdown blockquote)."""
    return ">" + text.replace("\n", "\n>")
