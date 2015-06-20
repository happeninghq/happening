# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_auto_20150608_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='upcoming_notification_1_sent',
        ),
        migrations.RemoveField(
            model_name='event',
            name='upcoming_notification_2_sent',
        ),
    ]
