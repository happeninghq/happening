"""Move groups into plugin."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def group_to_plugin(apps, schema_editor):
    """Move groups into plugin."""
    from plugins.groups.models import Group, TicketInGroup
    from events.models import EventSolution, Ticket
    # Group = apps.get_model("groups", "Group")
    # TicketInGroup = apps.get_model("groups", "TicketInGroup")
    # EventSolution = apps.get_model("events", "EventSolution")
    # Ticket = apps.get_model("events", "ticket")

    for event_solution in EventSolution.objects.all():
        group = Group(
            event=event_solution.event,
            team_number=event_solution.team_number,
            team_name=event_solution.team_name,
            description=event_solution.description,
            github_url=event_solution.github_url)
        group.save()

        for ticket in Ticket.objects.filter(event=group.event, group=group.team_number):
            ticket_in_group = TicketInGroup(group=group, ticket=ticket)
            ticket_in_group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_event_title'),
    ]

    operations = [
        migrations.RunPython(group_to_plugin)
    ]
