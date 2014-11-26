# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='cancelled',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
