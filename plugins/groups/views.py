"""Group views."""
from django.shortcuts import render, get_object_or_404, redirect
from happening.utils import staff_member_required
from events.models import Event, Ticket
from django.contrib import messages
from .forms import GroupGenerationForm, GroupForm, ChangeGroupForm
from .models import Group, TicketInGroup
from plugins.groups import generate_groups as generate_groups_func
from django.core.exceptions import PermissionDenied
from .notifications import GroupEditedNotification
from .templatetags.group_permissions import can_create_group
from .templatetags.group_permissions import can_move_groups
from .templatetags.group_permissions import can_edit_groups
from happening.configuration import get_configuration_variables
from happening.configuration import attach_to_form
from happening.configuration import save_variables
from plugins.groups.event_configuration import GroupProperties
from plugins.groups.group_form import CustomProperties


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


@staff_member_required
def change_group(request, pk):
    """Change an attendee's group."""
    ticket = get_object_or_404(Ticket, pk=pk)
    current_group_id = None
    if ticket.group():
        current_group_id = ticket.group().pk
    form = ChangeGroupForm(groups=ticket.event.groups(),
                           initial={"group": current_group_id})
    if request.method == "POST":
        form = ChangeGroupForm(
            request.POST,
            groups=ticket.event.groups(),
            initial={"group": current_group_id})
        if form.is_valid():
            if ticket.group():
                ticket.group().remove_user(ticket.user)
            if form.cleaned_data['group']:
                form.cleaned_data['group'].add_user(ticket.user)
                messages.success(
                    request,
                    "%s moved to %s." % (ticket.user,
                                         form.cleaned_data['group']))
            else:
                messages.success(request,
                                 "%s removed from group." % ticket.user)
            return redirect("staff_event", ticket.event.pk)
    return render(request, "groups/staff/change_group.html",
                  {"ticket": ticket, "form": form})


def add_group(request, pk):
    """Add a group."""
    event = get_object_or_404(Event, pk=pk)
    form = GroupForm()
    ticket = request.user.tickets.filter(event=event, cancelled=False).first()
    if not can_create_group(request.user, event):
        return redirect("groups", event.pk)
    variables = get_configuration_variables("group_form",
                                            event=event)
    attach_to_form(form, variables)

    if request.method == "POST":
        form = GroupForm(request.POST)
        attach_to_form(form, variables)
        if form.is_valid():
            group = form.save(commit=False)
            group.event = event
            group.team_number = Group.objects.filter(event=event).count() + 1
            group.save()
            variables = get_configuration_variables(
                "group_form", group, event=event)
            save_variables(form, variables)

            # Add the user to the group
            ticket = request.user.tickets.filter(event=event).first()
            TicketInGroup(ticket=ticket, group=group).save()

            messages.success(request, "The group has been created.")
            return redirect("groups", event.pk)
    return render(request, "groups/add_group.html",
                  {"form": form, "event": event})


def groups(request, pk):
    """List groups."""
    event = get_object_or_404(Event, pk=pk)

    return render(request, "groups/groups.html",
                  {"event": event})


def view_group(request, pk, group_number):
    """Edit a group."""
    event = get_object_or_404(Event, pk=pk)
    group = event.raw_groups.filter(team_number=group_number).first()

    group_properties = GroupProperties(event).get()
    custom_properties = CustomProperties(group).get()

    return render(request, "groups/view_group.html",
                  {"event": event, "group": group,
                   "group_properties": group_properties,
                   "custom_properties": custom_properties})


def edit_group(request, pk, group_number):
    """Edit a group."""
    event = get_object_or_404(Event, pk=pk)
    group = event.raw_groups.filter(team_number=group_number).first()
    if not can_edit_groups(request.user, event):
        return redirect("groups", event.pk)
    if not group.is_editable_by(request.user):
        raise PermissionDenied()
    variables = get_configuration_variables("group_form", group,
                                            event=event)
    form = GroupForm(instance=group)
    attach_to_form(form, variables)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        attach_to_form(form, variables)
        if form.is_valid():
            form.save()
            save_variables(form, variables)
            for member in group.members():
                GroupEditedNotification(
                    member,
                    event=event,
                    group_name=str(group),
                    user=request.user,
                    user_name=str(request.user),
                    user_photo_url=request.user.profile.photo_url()
                ).send()
            messages.success(request, "The group has been updated.")
            return redirect("groups", event.pk)
    return render(request, "groups/edit_group.html",
                  {"event": event, "group": group, "form": form})


def join_group(request, pk, group_number):
    """Join a group."""
    event = get_object_or_404(Event, pk=pk)
    group = event.raw_groups.filter(team_number=group_number).first()

    if not can_move_groups(request.user, event):
        return redirect("groups", event.pk)

    if group.add_user(request.user):
        messages.success(request, "You have joined the group")

    return redirect("groups", event.pk)


def leave_group(request, pk, group_number):
    """Leave a group."""
    event = get_object_or_404(Event, pk=pk)
    group = event.raw_groups.filter(team_number=group_number).first()

    if not can_move_groups(request.user, event):
        return redirect("groups", event.pk)

    if group.remove_user(request.user):
        messages.success(request, "You have left the group")
    return redirect("groups", event.pk)
