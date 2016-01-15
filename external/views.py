"""External views."""

from django.shortcuts import render, redirect
from events.models import Event
from pages.configuration import PrimaryEvent


def index(request):
    """Homepage."""
    primary_event = PrimaryEvent()
    if primary_event.is_enabled():
        event = Event.objects.filter(pk=primary_event.get()).first()
        if event:
            return redirect("view_event", event.pk)

    events = Event.objects.order_by('-start')
    # TODO: Partition function or something?
    future_events = [e for e in events if e.is_future]
    past_events = [e for e in events if not e.is_future]

    return render(request, "index.html",
                  {"future_events": future_events,
                   "past_events": past_events})
