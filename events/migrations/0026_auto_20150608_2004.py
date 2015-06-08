"""Migrate dojo specific fields."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_dojo_fields(apps, schema_editor):
    """Migrate dojo specific fields."""
    from events.models import Event
    # for event in Event.objects.all():
    #     event.title = event.heading()
    #     x = ""
    #     if event._data.get('description'):
    #         x = event._data['description']
    #     if event.challenge_text:
    #         x += event.challenge_text + "\n\n"
    #     if event.solution_text:
    #         x += event.solution_text
    #     event._data['description'] = x
    #     event.save()


class Migration(migrations.Migration):

    """Remove dojo specific fields."""

    dependencies = [
        ('events', '0025_auto_20150528_1959'),
    ]

    operations = [
        migrations.RunPython(migrate_dojo_fields)
    ]
