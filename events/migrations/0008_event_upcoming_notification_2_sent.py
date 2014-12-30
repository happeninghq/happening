# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event_upcoming_notification_1_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='upcoming_notification_2_sent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
