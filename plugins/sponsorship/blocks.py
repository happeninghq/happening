"""Sponsorship template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string
from models import CommunitySponsorship


@plugin_block("events.event_long")
def event_long(request, event):
    """Add sponsorship information to long event information."""
    return render_to_string("sponsorship/blocks/events/event_long.html",
                            {"event": event})


@plugin_block("events.event_short")
def event_short(request, event):
    """Add sponsorship information to short event information."""
    # Same as long
    return event_long(request, event)


@plugin_block("staff.event")
def staff_event(request, event):
    """Add sponsorship links to staff event."""
    return render_to_string("sponsorship/blocks/staff/event.html",
                            {"event": event})


@plugin_block("index.secondary_content")
def community_sponsors(request):
    """Add community sponsor links to footer."""
    from models import SponsorTier

    if CommunitySponsorship.objects.count() == 0:
        # No sponsors, don't show it
        return ""

    return render_to_string(
        "sponsorship/blocks/index/secondary_content.html",
        {"sponsor_tiers": SponsorTier.objects.all()})
