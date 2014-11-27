""" Event views. """
from django.shortcuts import render, get_object_or_404
from models import Event
from django.http import Http404
from django.contrib.auth.decorators import login_required


def view(request, pk):
    """ View an event (typically a past event). """
    event = get_object_or_404(Event, pk=pk)
    if event.is_future():
        raise Http404
    return render(request, "events/view.html", {"event": event})


@login_required
def purchase_tickets(request, pk):
    """ Purchase tickets for an event. """
    pass
