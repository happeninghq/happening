""" Event views. """
from django.shortcuts import render
from models import Event


def view(request, pk):
    """ View an event (typically a past event). """
    event = Event.objects.get(pk=pk)
    return render(request, "events/view.html", {"event": event})
