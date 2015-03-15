"""External views."""

from django.shortcuts import render
from events.models import Event


def index(request):
    """Homepage."""
    latest_event = Event.objects.latest_event
    return render(request, "index.html", {"latest_event": latest_event})
