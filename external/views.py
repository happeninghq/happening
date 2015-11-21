"""External views."""

from django.shortcuts import render, redirect
from events.models import Event
from django.utils import timezone
from pages.configuration import PrimaryEvent


def index(request):
    """Homepage."""
    primary_event = PrimaryEvent().get()
    event = Event.objects.filter(pk=primary_event).first()
    if event:
        return redirect("view_event", event.pk)

    now = timezone.now()
    return render(request, "index.html",
                  {"future_events": Event.objects.filter(start__gt=now)
                   .order_by('start'),
                   "past_events": Event.objects.filter(start__lt=now)
                   .order_by('-start')})
