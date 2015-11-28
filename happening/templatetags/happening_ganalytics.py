"""A simple Django templatetag that renders Google Analytics code."""

from pages.configuration import GoogleAnalyticsCode
from django import template
from django.template import Context
from django.template.loader import get_template


register = template.Library()


@register.simple_tag
def ganalytics():
    """Render Google Analytics tracking code from configuration variable."""
    if not GoogleAnalyticsCode().is_enabled():
        return ""

    ga_code = GoogleAnalyticsCode().get()
    if not ga_code:
        return ""
    context = Context({'GANALYTICS_TRACKING_CODE': ga_code})
    return get_template('ganalytics/ganalytics.js').render(context)
