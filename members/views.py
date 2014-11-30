""" Member views. """

from django.shortcuts import render, get_object_or_404, redirect
from events.models import Ticket
from events.forms import TicketForm
from django.http import Http404
from django.contrib.auth.decorators import login_required


@login_required
def my_tickets(request):
    """ List tickets I have purchased. """
    return render(request, "members/my_tickets.html")


@login_required
def edit_ticket(request, pk):
    """ Edit the quantity of tickets. """
    ticket = get_object_or_404(Ticket, pk=pk)

    if not ticket.user == request.user:
        raise Http404

    if not ticket.event.is_future():
        return redirect("my_tickets")

    max_tickets = ticket.event.remaining_tickets + ticket.number + 1

    form = TicketForm(event=ticket.event,
                      initial={"quantity": ticket.number},
                      max_tickets=max_tickets)

    if request.method == "POST":
        form = TicketForm(request.POST,
                          event=ticket.event,
                          max_tickets=max_tickets)
        if form.is_valid():
            ticket.number = form.cleaned_data['quantity']
            ticket.save()
            return redirect("my_tickets")

    return render(request, "members/edit_ticket.html",
                  {"ticket": ticket, "form": form})


@login_required
def cancel_ticket(request, pk):
    """ Cancel a ticket. """
    ticket = get_object_or_404(Ticket, pk=pk)

    if not ticket.user == request.user:
        raise Http404

    if not ticket.event.is_future():
        return redirect("my_tickets")

    if request.method == "POST":
        ticket.cancel()
        return redirect("my_tickets")

    return render(request, "members/cancel_ticket.html", {"ticket": ticket})
