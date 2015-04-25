"""Groups template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string


@plugin_block("events.event_long")
def event_long(request, event):
    """Add groups to long event information."""
    return render_to_string("groups/blocks/events/event_long.html",
                            {"event": event})
