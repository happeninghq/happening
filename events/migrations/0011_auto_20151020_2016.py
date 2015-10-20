# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20150922_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettype',
            name='waiting_list_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
    ]
