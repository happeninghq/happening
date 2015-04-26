"""Groups template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string


@plugin_block("events.event_long")
def event_long(request, event):
    """Add groups to long event information."""
    return render_to_string("groups/blocks/events/event_long.html",
                            {"event": event})


@plugin_block("staff.event.tickets.headers")
def staff_event_tickets_headers(request, event, ticket):
    """Add group header to ticket lists on event."""
    return render_to_string("groups/blocks/staff/event/tickets/headers.html",
                            {"event": event, "ticket": ticket})


@plugin_block("staff.event.tickets.info")
def staff_event_tickets_info(request, event, ticket):
    """Add group info to tickets on event list."""
    return render_to_string("groups/blocks/staff/event/tickets/info.html",
                            {"event": event, "ticket": ticket})


@plugin_block("staff.event.buttons")
def staff_event_buttons(request, event):
    """Add generate group button on event."""
    return render_to_string("groups/blocks/staff/event/buttons.html",
                            {"event": event})
