"""Event navigation items."""
from happening.plugins import register_navigation_item
from django.template.loader import render_to_string


@register_navigation_item(key="events", name="Events")
def events_navigation_item(request, context):
    """Link to events category."""
    return render_to_string("events/navigation_items/events.html", context,
                            request=request)
