# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150920_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketorder',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
    ]
