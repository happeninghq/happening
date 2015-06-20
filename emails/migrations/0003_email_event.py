# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_auto_20150620_0914'),
        ('emails', '0002_auto_20150614_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='event',
            field=models.ForeignKey(to='events.Event', null=True),
        ),
    ]
