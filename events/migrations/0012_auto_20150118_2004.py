# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150117_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsolution',
            name='team_number',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventsolution',
            name='team_name',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
