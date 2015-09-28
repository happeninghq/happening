"""Sponsorship template blocks."""
from happening.plugins import plugin_block
from django.template.loader import render_to_string
from models import CommunitySponsorship


@plugin_block("events.event.secondary_content")
def event_secondary_content(request, event):
    """Add sponsorship information to event page."""
    if not event.sponsor():
        return ""
    return render_to_string(
        "sponsorship/blocks/events/event/secondary_content.html",
        {"event": event})


@plugin_block("staff.event")
def staff_event(request, event):
    """Add sponsorship links to staff event."""
    return render_to_string("sponsorship/blocks/staff/event.html",
                            {"event": event})


@plugin_block("index.secondary_content")
def community_sponsors(request):
    """Add community sponsor links to sidebar."""
    from models import SponsorTier

    if CommunitySponsorship.objects.count() == 0:
        # No sponsors, don't show it
        return ""

    return render_to_string(
        "sponsorship/blocks/index/secondary_content.html",
        {"sponsor_tiers": SponsorTier.objects.all()})
