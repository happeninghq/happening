# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import happening.db


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0029_event_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=happening.db.AddressField(null=True),
        ),
    ]
