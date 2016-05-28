"""Sponsorship template blocks."""
from happening.plugins import plugin_block
from happening.utils import render_block
from .models import CommunitySponsorship
from .forms import EventSponsorForm


@plugin_block("events.event.secondary_content")
def event_secondary_content(request, event):
    """Add sponsorship information to event page."""
    if event.event_sponsors.count() == 0:
        return ""
    return render_block(
        request,
        "sponsorship/blocks/events/event/secondary_content.html",
        {"event": event})


@plugin_block("staff.event")
def staff_event(request, event):
    """Add sponsorship links to staff event."""
    return render_block(
        request,
        "sponsorship/blocks/staff/event.html",
        {"event": event,
         "event_sponsor_form": EventSponsorForm(event=event)})


@plugin_block("index.secondary_content")
def community_sponsors(request):
    """Add community sponsor links to sidebar."""
    from .models import SponsorTier

    if CommunitySponsorship.objects.count() == 0:
        # No sponsors, don't show it
        return ""

    return render_block(
        request,
        "sponsorship/blocks/index/secondary_content.html",
        {"sponsor_tiers": SponsorTier.objects.all()})
