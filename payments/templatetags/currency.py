"""Template tags relating to currency."""

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.html import mark_safe

register = template.Library()


@register.filter()
def format_currency(pennies):
    """Format pennies as currency."""
    pennies = float(pennies) / 100.0
    pennies = round(float(pennies), 2)

    if pennies < 0:
        pennies = 0 - pennies
        return mark_safe("-&pound;%s%s" % (intcomma(int(pennies)),
                                           ("%0.2f" % pennies)[-3:]))
    return mark_safe("&pound;%s%s" % (intcomma(int(pennies)),
                                      ("%0.2f" % pennies)[-3:]))
