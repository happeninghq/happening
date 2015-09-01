"""Sponsorship template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string
from django.template import RequestContext


@plugin_block("events.event.secondary_navigation")
def event_secondary_navigation(request, secondary_nav, event):
    """Add discussion to event page."""
    return render_to_string(
        "comments/blocks/events/event/secondary_navigation.html",
        {"secondary_nav": secondary_nav, "event": event},
        context_instance=RequestContext(request))


@plugin_block("events.event_block.small_info")
def event_block_small_info(request, event):
    """Add comment count to event block."""
    return render_to_string(
        "comments/blocks/events/event_block/small_info.html",
        {"event": event}, context_instance=RequestContext(request))


@plugin_block("events.event.primary_content")
def event_primary_content(request, event):
    """Add discussion to event info."""
    recent_comments = [a for a in reversed(event.comments())][:3]
    return render_to_string(
        "comments/blocks/events/event/primary_content.html",
        {"event": event, "recent_comments": recent_comments},
        context_instance=RequestContext(request))
