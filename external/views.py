"""External views."""

from django.shortcuts import render
from events.models import Event
from django.utils import timezone


def index(request):
    """Homepage."""
    now = timezone.now()
    return render(request, "index.html",
                  {"future_events": Event.objects.filter(start__gt=now)
                   .order_by('start'),
                   "past_events": Event.objects.filter(start__lt=now)
                   .order_by('-start')})
