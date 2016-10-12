"""Nottification navigation items."""
from happening.plugins import register_navigation_item
from django.template.loader import render_to_string


@register_navigation_item(key="notifications")
def notifications_navigation_item(request, context):
    """Link to notifications category."""
    return render_to_string(
        "notifications/navigation_items/notifications.html", context,
        request=request)
