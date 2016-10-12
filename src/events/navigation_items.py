"""Event navigation items."""
from happening.plugins import register_navigation_item
from django.template.loader import render_to_string


@register_navigation_item(key="events")
def events_navigation_item(request):
    """Link to events category."""
    return render_to_string("events/navigation_items/events.html",
                            request=request)
