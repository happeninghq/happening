"""Group views."""
from django.shortcuts import render, get_object_or_404, redirect
from happening.utils import staff_member_required
from events.models import Event
from django.contrib import messages
from forms import GroupGenerationForm, GroupForm
from models import Group, TicketInGroup
from plugins.groups import generate_groups as generate_groups_func
from django.core.exceptions import PermissionDenied


def event_to_existing_groups(event):
    """Flatten django models into a dictionary for tickets > groups."""
    existing_groups = {}
    for group in event.raw_groups.all():
        existing_groups[group.team_number - 1] =\
            [t.ticket for t in group.tickets.all()]
    return existing_groups


def delete_all_group_membership(event):
    """Delete membership of all groups from the database."""
    for group in event.raw_groups.all():
        for ticket in group.tickets.all():
            ticket.delete()


def delete_existing_groups(event):
    """Delete existing groups."""
    for group in event.raw_groups.all():
        group.delete()


@staff_member_required
def generate_groups(request, pk):
    """Generate groups."""
    event = get_object_or_404(Event, pk=pk)
    form = GroupGenerationForm()

    if request.method == "POST":
        # Generate the groups
        form = GroupGenerationForm(request.POST)
        if form.is_valid():
            # Clear existing groups if needed
            if form.cleaned_data['clear_existing_groups']:
                delete_existing_groups(event)

            number_of_groups = form.cleaned_data['number_of_groups']
            ungrouped_tickets = event.ungrouped_tickets()

            if form.cleaned_data['only_group_checked_in']:
                ungrouped_tickets = [t for t in ungrouped_tickets
                                     if t.checked_in]

            existing_groups = event_to_existing_groups(event)

            groups = generate_groups_func(ungrouped_tickets, number_of_groups,
                                          existing_groups)

            # Delete old group membership from database
            delete_all_group_membership(event)

            group_models = {}
            # Write the groups to database
            for i in range(1, number_of_groups + 1):
                group_models[i] = Group.objects.get_or_create(event=event,
                                                              team_number=i)[0]

            # Write group membership to database
            for i, g in enumerate(groups, 1):
                for ticket in g:
                    TicketInGroup(group=group_models[i], ticket=ticket).save()

            messages.success(request, "Groups have been generated.")
            return redirect("staff_event", event.pk)

    checked_in_attendees = [t for t in event.tickets.all()
                            if t.checked_in and not t.cancelled]
    return render(request, "groups/staff/generate_groups.html",
                  {"event": event, "form": form,
                   "checked_in_attendees": checked_in_attendees})


@staff_member_required
def view_groups(request, pk):
    """View groups."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, "groups/staff/view_groups.html",
                  {"event": event})


def add_group(request, pk):
    """Add a group."""
    event = get_object_or_404(Event, pk=pk)
    form = GroupForm()
    ticket = request.user.tickets.filter(event=event, cancelled=False).first()
    if not ticket or ticket.groups.count() > 0:
        # We don't have a ticket or are already in a group
        return redirect("view_event", event.pk)

    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.event = event
            # TODO: Get next team number
            group.team_number = 2
            group.save()

            # Add the user to the group
            ticket = request.user.tickets.filter(event=event).first()
            TicketInGroup(ticket=ticket, group=group).save()

            messages.success(request, "The group has been created.")
            return redirect("view_event", event.pk)
    return render(request, "groups/add_group.html",
                  {"form": form, "event": event})


def edit_group(request, pk, group_number):
    """Edit a group."""
    event = get_object_or_404(Event, pk=pk)
    group = event.raw_groups.filter(team_number=group_number).first()
    if not group.is_editable_by(request.user):
        raise PermissionDenied()
    form = GroupForm(instance=group)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            # TODO: Notifications
            messages.success(request, "The group has been updated.")
            return redirect("view_event", event.pk)
    return render(request, "groups/edit_group.html",
                  {"group": group, "form": form})


def join_group(request, pk, group_number):
    """Join a group."""
    event = get_object_or_404(Event, pk=pk)
    group = event.raw_groups.filter(team_number=group_number).first()

    ticket = request.user.tickets.filter(event=event, cancelled=False).first()
    if ticket:
        if ticket.groups.count() == 0:
            # No groups yet
            ticket = request.user.tickets.get(event=event, cancelled=False)
            TicketInGroup(group=group, ticket=ticket).save()
            messages.success(request, "You have joined the group")
    return redirect("view_event", event.pk)


def leave_group(request, pk, group_number):
    """Leave a group."""
    event = get_object_or_404(Event, pk=pk)
    group = event.raw_groups.filter(team_number=group_number).first()
    ticket_in_group = group.tickets.filter(ticket__user=request.user).first()
    if ticket_in_group:
        ticket_in_group.delete()
        messages.success(request, "You have left the group")
    return redirect("view_event", event.pk)
