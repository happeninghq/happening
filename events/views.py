""" Event views. """
from django.shortcuts import render, get_object_or_404, redirect
from models import Event, Ticket, EventSolution
from django.http import Http404
from django.contrib.auth.decorators import login_required
from forms import TicketForm, GroupNumberForm
from forms import GroupSubmissionForm
from django.utils import timezone
from django.views.decorators.http import require_POST
import json


def view(request, pk):
    """ View an event (typically a past event). """
    event = get_object_or_404(Event, pk=pk)

    group_form = GroupNumberForm()
    group_submission_form = GroupSubmissionForm()

    return render(request,
                  "events/view.html",
                  {"event": event,
                   "group_form": group_form,
                   "group_submission_form": group_submission_form
                   })


@login_required
def purchase_tickets(request, pk):
    """ Purchase tickets for an event. """
    event = get_object_or_404(Event, pk=pk)

    if not event.is_future:
        return redirect("view_event", event.pk)

    if event.remaining_tickets == 0:
        return redirect("view_event", event.pk)

    form = TicketForm(event=event)
    if request.method == "POST":
        form = TicketForm(request.POST, event=event)
        if form.is_valid():
            ticket = event.buy_ticket(request.user,
                                      int(form.cleaned_data['quantity']))
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


def events(request):
    """ List events. """
    events = Event.objects.all().order_by("-datetime")
    return render(request, "events/events.html",
                  {"all_events": events})


@require_POST
@login_required
def vote(request, pk):
    """ Vote for languages for an event. """
    event = get_object_or_404(Event, pk=pk)

    if not event.is_voting:
        return redirect("view_event", event.pk)

    # Check that we have tickets
    ticket = event.tickets.get(user=request.user, cancelled=False)
    if not ticket:
        return redirect("view_event", event.pk)

    # Record the vote
    ticket.votes = json.loads(request.POST['languages'])
    ticket.save()

    return redirect("view_event", event.pk)


@require_POST
@login_required
def set_group(request, pk):
    """ Set the group the member was in at an event. """
    event = get_object_or_404(Event, pk=pk)

    if event.is_future:
        return redirect("view_event", event.pk)

    # Check that we have tickets
    tickets = event.tickets.filter(user=request.user, cancelled=False)
    if len(tickets) < 1:
        return redirect("view_event", event.pk)

    # Record the group
    form = GroupNumberForm(request.POST)

    if form.is_valid():
        for t in tickets:
            # We update it for all tickets as we can't separate them
            if form.cleaned_data['group_number'] == "0":
                t.did_not_attend = True
            else:
                t.group = form.cleaned_data['group_number']
            t.save()

    return redirect("view_event", event.pk)


@require_POST
@login_required
def group_submission(request, pk):
    """ Set the group info for the current member's group. """
    event = get_object_or_404(Event, pk=pk)

    if event.is_future:
        return redirect("view_event", event.pk)

    # Check that we have tickets
    tickets = event.tickets.filter(user=request.user, cancelled=False)
    if len(tickets) < 1:
        return redirect("view_event", event.pk)

    ticket = tickets[0]
    if not ticket.group:
        return redirect("view_event", event.pk)

    # Record the group information
    form = GroupSubmissionForm(request.POST)

    if form.is_valid():
        group = EventSolution.objects.get_or_create(
            event=event, team_number=ticket.group)[0]
        group.description = form.cleaned_data['description']
        group.github_url = form.cleaned_data['github_url']
        group.save()
        return redirect("view_event", event.pk)

    return render(request,
                  "events/view.html",
                  {"event": event,
                   "group_submission_form": form
                   })
