"""Sponsorship views."""
from django.shortcuts import render, get_object_or_404, redirect
from models import Sponsor, EventSponsor, SponsorTier, CommunitySponsorship
from happening.utils import staff_member_required, admin_required
from forms import SponsorForm, EventSponsorForm, SponsorTierForm
from forms import CommunitySponsorshipForm
from events.models import Event


def view_sponsor(request, pk):
    """View a sponsor's profile."""
    sponsor = get_object_or_404(Sponsor, pk=pk)
    return render(request, "sponsorship/view.html",
                  {"sponsor": sponsor})


@staff_member_required
def sponsors(request):
    """Administrate sponsors."""
    sponsors = Sponsor.objects.all()
    return render(request, "sponsorship/staff/sponsors.html",
                  {"sponsors": sponsors})


@staff_member_required
def staff_view_sponsor(request, pk):
    """View sponsor as staff."""
    sponsor = get_object_or_404(Sponsor, pk=pk)
    return render(request, "sponsorship/staff/view.html",
                  {"sponsor": sponsor})


@staff_member_required
def add_community_sponsorship_to_sponsor(request, pk):
    """Add a community sponsorship to a sponsor."""
    sponsor = get_object_or_404(Sponsor, pk=pk)
    form = CommunitySponsorshipForm()
    if request.method == "POST":
        form = CommunitySponsorshipForm(request.POST)
        if form.is_valid():
            e = CommunitySponsorship(
                sponsor=sponsor, tier=form.cleaned_data['tier'])
            e.save()

            return redirect("staff_view_sponsor", sponsor.pk)
    return render(request, "sponsorship/staff/" +
                  "add_community_sponsorship_to_sponsor.html",
                  {"form": form, "sponsor": sponsor})


@staff_member_required
def edit_sponsor(request, pk):
    """Edit sponsor."""
    sponsor = get_object_or_404(Sponsor, pk=pk)
    form = SponsorForm(instance=sponsor)
    if request.method == "POST":
        form = SponsorForm(request.POST, request.FILES, instance=sponsor)
        if form.is_valid():
            form.save()
            return redirect("staff_sponsors")
    return render(request, "sponsorship/staff/edit_sponsor.html",
                  {"sponsor": sponsor, "form": form})


@staff_member_required
def create_sponsor(request):
    """Create sponsor."""
    form = SponsorForm()
    if request.method == "POST":
        form = SponsorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("staff_sponsors")
    return render(request, "sponsorship/staff/create_sponsor.html",
                  {"form": form})


@admin_required
def sponsorship_tiers(request):
    """Administrate sponsorship tiers."""
    sponsorship_tiers = SponsorTier.objects.all()
    return render(request, "sponsorship/admin/sponsorship_tiers.html",
                  {"sponsorship_tiers": sponsorship_tiers})


@admin_required
def edit_sponsorship_tier(request, pk):
    """Edit sponsorship tier."""
    sponsorship_tier = get_object_or_404(SponsorTier, pk=pk)
    form = SponsorTierForm(instance=sponsorship_tier)
    if request.method == "POST":
        form = SponsorTierForm(request.POST, request.FILES,
                               instance=sponsorship_tier)
        if form.is_valid():
            form.save()
            return redirect("admin_sponsorship_tiers")
    return render(request, "sponsorship/admin/edit_sponsorship_tier.html",
                  {"sponsorship_tier": sponsorship_tier, "form": form})


@admin_required
def create_sponsorship_tier(request):
    """Create sponsorship_tier."""
    form = SponsorTierForm()
    if request.method == "POST":
        form = SponsorTierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_sponsorship_tiers")
    return render(request, "sponsorship/admin/create_sponsorship_tier.html",
                  {"form": form})


@staff_member_required
def edit_on_event(request, pk):
    """Edit the sponsor for an event."""
    event = get_object_or_404(Event, pk=pk)
    form = EventSponsorForm(initial={"sponsor": event.sponsor})
    if request.method == "POST":
        form = EventSponsorForm(request.POST)
        if form.is_valid():
            # First delete any existing event sponsor
            for e in event.event_sponsors.all():
                e.delete()

            # Then add the new one
            if form.cleaned_data['sponsor'] is not None:
                e = EventSponsor(
                    sponsor=form.cleaned_data['sponsor'], event=event)
                e.save()

            return redirect("staff_event", event.pk)
    return render(request, "sponsorship/staff/edit_on_event.html",
                  {"form": form, "event": event})
