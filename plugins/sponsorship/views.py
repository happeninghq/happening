"""Sponsorship views."""
from django.shortcuts import render, get_object_or_404, redirect
from models import Sponsor, EventSponsor
from happening.utils import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import SponsorForm, EventSponsorForm
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
    paginator = Paginator(sponsors, 10)

    page = request.GET.get('page')
    try:
        sponsors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sponsors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sponsors = paginator.page(paginator.num_pages)
    return render(request, "sponsorship/staff/sponsors.html",
                  {"sponsors": sponsors})


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
