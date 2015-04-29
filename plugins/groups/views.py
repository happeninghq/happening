"""Group views."""
from django.shortcuts import render, get_object_or_404, redirect
from happening.utils import staff_member_required
from events.models import Event
from django.contrib import messages
from forms import GroupGenerationForm
from models import Group, TicketInGroup
from plugins.groups import generate_groups as generate_groups_func


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
                for group in event.raw_groups.all():
                    group.delete()

            number_of_groups = form.cleaned_data['number_of_groups']
            ungrouped_tickets = event.ungrouped_tickets()

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
    return render(request, "groups/staff/generate_groups.html",
                  {"event": event, "form": form})


@staff_member_required
def view_groups(request, pk):
    """View groups."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, "groups/staff/view_groups.html",
                  {"event": event})
