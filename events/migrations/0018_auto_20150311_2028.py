# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20150308_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='site',
        ),
        migrations.RemoveField(
            model_name='eventsolution',
            name='site',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='site',
        ),
    ]
