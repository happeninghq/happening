# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('events', '0016_remove_event_sponsor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtodo',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='eventtodo',
            name='completed_by',
        ),
        migrations.RemoveField(
            model_name='eventtodo',
            name='event',
        ),
        migrations.DeleteModel(
            name='EventTodo',
        ),
        migrations.AddField(
            model_name='event',
            name='site',
            field=models.ForeignKey(default=1, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventsolution',
            name='site',
            field=models.ForeignKey(default=1, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='site',
            field=models.ForeignKey(default=1, to='sites.Site'),
            preserve_default=False,
        ),
    ]
