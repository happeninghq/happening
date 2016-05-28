"""Groups template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string
from django.template import RequestContext


@plugin_block("events.event.secondary_navigation")
def event_secondary_navigation(request, secondary_nav, event):
    """Add groups to event page."""
    return render_to_string(
        "groups/blocks/events/event/secondary_navigation.html",
        {"secondary_nav": secondary_nav, "event": event},
        context_instance=RequestContext(request))


@plugin_block("events.event.secondary_content")
def event_secondary_content(request, event):
    """Add groups to main event page."""
    return render_to_string(
        "groups/blocks/events/event/secondary_content.html",
        {"event": event},
        context_instance=RequestContext(request))


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
