"""Template tags relating to strings."""

from django import template
from happening.utils import convert_to_spaces
from django.utils.html import mark_safe

register = template.Library()


@register.filter()
def spaces(text):
    """Convert CamelCase into Space Separated."""
    return convert_to_spaces(text)


# Just a substring unlikely to occur so can be used as placeholder
UNUSED_SUBSTRING = "8734oflwehiu2873r87yor3f"


@register.filter()
def search(value, search):
    """Replace search with the unused substring."""
    return value.replace(search, UNUSED_SUBSTRING)
    # return re.sub(search, '#f4x@SgXXmS', value)


@register.filter()
def replace(value, replace):
    """Replace the unused substring with replace."""
    return value.replace(UNUSED_SUBSTRING, replace)
    # return re.sub('#f4x@SgXXmS', replace, value)


@register.filter()
def comma2br(text):
    """Convert CamelCase into Space Separated."""
    return mark_safe(text.replace(",", "<br />"))
