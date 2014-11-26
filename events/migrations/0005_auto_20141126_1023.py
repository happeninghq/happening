# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20141126_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='cancelled_datetime',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='last_edited_datetime',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 26, 10, 23, 29, 653971, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='purchased_datetime',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 26, 10, 23, 36, 149867, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='cancelled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
