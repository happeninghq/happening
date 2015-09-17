# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150917_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketorder',
            name='event',
            field=models.ForeignKey(related_name='order', default=1, to='events.Event'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
    ]
