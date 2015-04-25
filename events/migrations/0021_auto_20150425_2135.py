# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20150425_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventsolution',
            name='event',
        ),
        migrations.DeleteModel(
            name='EventSolution',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='group',
        ),
    ]
