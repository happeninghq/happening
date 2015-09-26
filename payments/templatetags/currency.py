"""Template tags relating to currency."""

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter()
def format_currency(pennies):
    """Format pennies as currency."""
    pennies = float(pennies) / 100.0
    pennies = round(float(pennies), 2)
    return "%s%s" % (intcomma(int(pennies)), ("%0.2f" % pennies)[-3:])
