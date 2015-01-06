""" Event views. """
from django.shortcuts import render, get_object_or_404, redirect
from models import Event, Ticket
from django.http import Http404
from django.contrib.auth.decorators import login_required
from forms import TicketForm
from django.utils import timezone


def view(request, pk):
    """ View an event (typically a past event). """
    event = get_object_or_404(Event, pk=pk)

    valid_tickets = []
    if request.user.is_authenticated():
        valid_tickets = [t for t in request.user.
                         tickets.filter(event=event, cancelled=False)]

    return render(request,
                  "events/view.html",
                  {"event": event,
                   "has_tickets": len(valid_tickets) > 0}
                  )


@login_required
def purchase_tickets(request, pk):
    """ Purchase tickets for an event. """
    event = get_object_or_404(Event, pk=pk)

    if not event.is_future():
        return redirect("view_event", event.pk)

    if event.remaining_tickets == 0:
        return redirect("view_event", event.pk)

    form = TicketForm(event=event)
    if request.method == "POST":
        form = TicketForm(request.POST, event=event)
        if form.is_valid():
            ticket = event.buy_ticket(request.user,
                                      form.cleaned_data['quantity'])
            return redirect("tickets_purchased", ticket.pk)
    return render(request, "events/purchase_tickets.html",
                  {"event": event, "form": form})


@login_required
def tickets_purchased(request, pk):
    """ Ticket has been purchased for an event. """
    ticket = get_object_or_404(Ticket, pk=pk)

    if not ticket.user == request.user:
        raise Http404

    # TODO: Ensure that this ticket belongs to this user
    return render(request, "events/tickets_purchased.html", {"ticket": ticket})


def previous_events(request):
    """ List previous events. """
    previous_events = Event.objects.filter(
        datetime__lte=timezone.now()).order_by("-datetime")
    return render(request, "events/previous_events.html",
                  {"previous_events": previous_events})
