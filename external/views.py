""" External views. """

from django.shortcuts import render
from events.models import Event
from django.utils import timezone


def index(request):
    """ Homepage. """
    # The latest event is EITHER the next event in the future (if there are
    # any) or the latest event in the past
    # TODO
    latest_event = Event.objects.latest_event
    previous_events = Event.objects.filter(
        datetime__lte=timezone.now()).order_by("datetime")

    return render(request, "index.html", {"latest_event": latest_event,
                                          "previous_events": previous_events})


def sponsorship(request):
    """ Sponsorship information, prices, etc. """
    return render(request, "sponsorship.html")
