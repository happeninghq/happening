""" External views. """

from django.shortcuts import render
from events.models import Event


def index(request):
    """ Homepage. """
    latest_event = Event.objects.latest_event
    return render(request, "index.html", {"latest_event": latest_event})


def sponsorship(request):
    """ Sponsorship information, prices, etc. """
    return render(request, "sponsorship.html")


def about(request):
    """ General information about the dojo. """
    return render(request, "about.html")
