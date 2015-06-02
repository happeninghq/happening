# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_paymenthandler'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='complete',
            new_name='_complete',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='status',
            new_name='_status',
        ),
        migrations.AddField(
            model_name='payment',
            name='complete_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='created_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 13, 32, 58, 13642, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='status_changed_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
