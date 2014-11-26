# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20141126_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='available_tickets',
            field=models.IntegerField(default=30),
            preserve_default=True,
        ),
    ]
