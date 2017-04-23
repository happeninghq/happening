"""Event views."""
from payments.decorators import payment_successful, payment_failed
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, TicketOrder, TicketType, RSVP
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import TicketForm
from django.utils import timezone
from payments.models import Payment
from django.contrib import messages
from events.event_configuration import MaxTicketsPerPerson


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

    # If there are no tickets we can buy, redirect
    tickets_available = sum([t.remaining_tickets for t in
                             event.ticket_types.purchasable_by(request.user)])
    if not tickets_available > 0:
        return redirect("view_event", event.pk)

    use_max_tickets = MaxTicketsPerPerson(event).is_enabled()

    if use_max_tickets:
        max_tickets = MaxTicketsPerPerson(event).get() -\
            event.tickets.filter(user=request.user, cancelled=False).count()
        form = TicketForm(event=event, max_tickets=max_tickets,
                          user=request.user)
    else:
        form = TicketForm(event=event, user=request.user)

    if request.method == "POST":
        if use_max_tickets:
            form = TicketForm(request.POST, event=event,
                              max_tickets=max_tickets, user=request.user)
        else:
            form = TicketForm(request.POST, event=event, user=request.user)
        if form.is_valid():
            tickets = {p[8:]: int(n) for p, n in
                       list(form.cleaned_data.items()) if
                       p.startswith("tickets_")}

            payment_required = event.total_ticket_cost(tickets)

            # If payment is required
            if payment_required > 0:
                # Now we need to put some tickets on hold -
                # and then pass to payment
                held_tickets = event.hold_tickets(request.user, tickets)

                # Create a payment
                payment = Payment(
                    user=request.user,
                    description="Tickets for %s" % str(event),
                    amount=payment_required,
                    extra={"event_pk": event.pk,
                           "held_tickets_pk": held_tickets.pk},
                    success_url_name="ticket_payment_success",
                    failure_url_name="ticket_payment_failure"
                )
                payment.save()
                return redirect("make_payment", payment.pk)

            order = event.buy_tickets(request.user,
                                      tickets)
            return redirect("tickets_purchased", order.pk)
    return render(request, "events/purchase_tickets.html",
                  {"event": event, "form": form})


@login_required
@payment_successful
def ticket_payment_success(request, payment):
    """Ticket payment successful."""
    order = get_object_or_404(TicketOrder, pk=payment.extra["held_tickets_pk"])
    order.mark_complete()

    return redirect("tickets_purchased", order.pk)


@login_required
@payment_failed
def ticket_payment_failure(request, payment):
    """Ticket payment failed."""
    messages.error(request, payment.error)
    return redirect("view_event", payment.extra["event_pk"])


@login_required
def tickets_purchased(request, pk):
    """Ticket has been purchased for an event."""
    order = get_object_or_404(TicketOrder, pk=pk)

    if not order.user == request.user:
        raise Http404

    if not order.complete:
        if not order.event.is_future:
            return redirect("view_event", order.event.pk)

        payment = Payment.objects.filter(
            _complete=False,
            extra__at_held_tickets_pk=order.pk
        ).first()

        if not payment:
            return redirect("view_event", order.event.pk)

        return redirect("make_payment", payment.pk)

    return render(request, "events/tickets_purchased.html", {
        "order": order, "event": order.tickets.first().event})


@require_POST
@login_required
def join_waiting_list(request, pk):
    """Join a waiting list."""
    ticket_type = get_object_or_404(TicketType, pk=pk,
                                    waiting_list_enabled=True)
    ticket_type.join_waiting_list(request.user)
    messages.success(request, "You have joined the waiting list")
    return redirect(request.GET.get("next", "index"))


@require_POST
@login_required
def leave_waiting_list(request, pk):
    """Leave a waiting list."""
    ticket_type = get_object_or_404(TicketType, pk=pk,
                                    waiting_list_enabled=True)
    ticket_type.leave_waiting_list(request.user)
    messages.success(request, "You have left the waiting list")
    return redirect(request.GET.get("next", "index"))


@login_required
def rsvp_going(request, pk):
    """Mark that a user is attending an event."""
    event = get_object_or_404(Event, pk=pk)

    if not request.method == "POST":
        return redirect("view_event", event.pk)

    if not event.uses_rsvps:
        return HttpResponseBadRequest("RSVPs are not enabled for this event.")

    rsvp = request.user.rsvps.filter(event=event).first()
    if not rsvp:
        rsvp = RSVP(user=request.user, event=event)
    rsvp.going = True
    rsvp.save()

    return redirect("rsvped_going", event.pk)


@login_required
def rsvped_going(request, pk):
    """Confirm a user is attending an event."""
    event = get_object_or_404(Event, pk=pk)
    if not event.uses_rsvps:
        return redirect("view", event.pk)

    rsvp = request.user.rsvps.filter(event=event, going=True).first()
    if not rsvp:
        return redirect("view", event.pk)

    return render(request, "events/rsvped.html", {"event": event})


@login_required
def rsvp_not_going(request, pk):
    """Mark that a user is not attending an event."""
    event = get_object_or_404(Event, pk=pk)

    if not request.method == "POST":
        return redirect("view_event", event.pk)

    if not event.uses_rsvps:
        return HttpResponseBadRequest("RSVPs are not enabled for this event.")

    rsvp = request.user.rsvps.filter(event=event).first()
    if not rsvp:
        rsvp = RSVP(user=request.user, event=event)
    rsvp.going = False
    rsvp.save()

    messages.success(request,
                     "You have indicated you are not attending the event.")

    return redirect("view_event", event.pk)


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
