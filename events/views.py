"""Event views."""
from django.shortcuts import render, get_object_or_404, redirect
from models import Event, TicketOrder
from django.http import Http404
from django.contrib.auth.decorators import login_required
from forms import TicketForm
from django.utils import timezone


def view(request, pk):
    """View an event."""
    event = get_object_or_404(Event, pk=pk)

    return render(request,
                  "events/view.html",
                  {"event": event})


def view_attendees(request, pk):
    """View event attendees."""
    event = get_object_or_404(Event, pk=pk)
    return render(request,
                  "events/attendees.html",
                  {"event": event})


@login_required
def purchase_tickets(request, pk):
    """Purchase tickets for an event."""
    event = get_object_or_404(Event, pk=pk)

    if not event.is_future:
        return redirect("view_event", event.pk)

    if event.remaining_tickets == 0:
        return redirect("view_event", event.pk)

    form = TicketForm(event=event)
    if request.method == "POST":
        form = TicketForm(request.POST, event=event)
        if form.is_valid():
            order = event.buy_ticket(request.user,
                                     int(form.cleaned_data['quantity']))
            return redirect("tickets_purchased", order.pk)
    return render(request, "events/purchase_tickets.html",
                  {"event": event, "form": form})


@login_required
def tickets_purchased(request, pk):
    """Ticket has been purchased for an event."""
    order = get_object_or_404(TicketOrder, pk=pk)

    if not order.user == request.user:
        raise Http404

    return render(request, "events/tickets_purchased.html", {
        "order": order, "event": order.tickets.first().event})


def upcoming_events(request):
    """Upcoming events."""
    events = Event.objects.filter(start__gt=timezone.now()).order_by("-start")
    return render(request, "events/events.html",
                  {"events": events, "secondary_nav": "events"})


def past_events(request):
    """Past events."""
    events = Event.objects.filter(start__lt=timezone.now()).order_by("-start")
    return render(request, "events/events.html",
                  {"events": events, "secondary_nav": "past_events"})


def feeds(request):
    """List feeds."""
    return render(request, "events/feeds.html")
