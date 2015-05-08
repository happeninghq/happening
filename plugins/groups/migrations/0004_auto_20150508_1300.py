"""Move github urls into custom properties."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
import json


def migrate_github_urls(apps, schema_editor):
    """Move github urls into custom properties."""
    # First, for each event - if there are no group properties - add them
    from happening.models import ConfigurationVariable
    Event = apps.get_model("events", "Event")

    contenttype = ContentType.objects.get_for_model(Event)
    for event in Event.objects.all():
        c = ConfigurationVariable.objects.get_or_create(
            content_type=contenttype,
            object_id=event.id,
            key="group_properties")[0]

        if not c.value:
            c.value = json.dumps([{"type": "URLField", "name": "Github URL"}])
            c.save()

    # Then convert the github url for each group
    Group = apps.get_model("groups", "Group")
    contenttype = ContentType.objects.get_for_model(Group)

    for group in Group.objects.all():
        c = ConfigurationVariable.objects.get_or_create(
            content_type=contenttype,
            object_id=group.id,
            key="custom_properties")[0]

        if not c.value:
            c.value = json.dumps({"github_url": group.github_url})
            c.save()




class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20150426_1231'),
    ]

    operations = [
        migrations.RunPython(migrate_github_urls),
    ]
