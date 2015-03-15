"""Sponsorship template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string


@plugin_block("events.event_long")
def event_long(event):
    """Add sponsorship information to long event information."""
    return render_to_string("sponsorship/blocks/events/event_long.html",
                            {"event": event})


@plugin_block("events.event_short")
def event_short(event):
    """Add sponsorship information to short event information."""
    # Same as long
    return event_long(event)


@plugin_block("staff.event")
def staff_event(event):
    """Add sponsorship links to staff event."""
    return render_to_string("sponsorship/blocks/staff/event.html",
                            {"event": event})
