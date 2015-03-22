"""Sponsorship template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string
from django.template import RequestContext


@plugin_block("events.event_long")
def event_long(request, event):
    """Add comments to event."""
    return render_to_string("comments/blocks/events/event_long.html",
                            {"event": event}, RequestContext(request))
