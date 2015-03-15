"""Merge multiple tickets for an event into a single ticket."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth import get_user_model


def merge_tickets(apps, schema_editor):
    """Merge multiple tickets for an event into a single ticket."""
    User = get_user_model()
    for user in User.objects.all():
        members_tickets = user.tickets.all()
        # First, separate the tickets into bins according to which
        # event they are for
        events = {}
        for ticket in members_tickets:
            # Leave cancelled tickets alone
            if not ticket.cancelled:
                if ticket.event not in events:
                    events[ticket.event] = []
                events[ticket.event].append(ticket)

        # If any events have more than one ticket we need to merge them
        for event, tickets in events.items():
            if len(tickets) > 1:
                # Merge
                ticket = tickets[0]
                for i in range(1, len(tickets)):
                    ticket.number += tickets[i].number
                    tickets[i].delete()
                ticket.save()


class Migration(migrations.Migration):

    """Merge multiple tickets for an event into a single ticket."""

    dependencies = [
        ('events', '0014_eventtodo'),
    ]

    operations = [
        migrations.RunPython(merge_tickets),
    ]
