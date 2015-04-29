# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_auto_20150425_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='checked_in',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='checked_in_datetime',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
