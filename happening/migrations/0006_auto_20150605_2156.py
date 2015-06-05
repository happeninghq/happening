# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0005_auto_20150530_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='happeningsite',
            name='primary_colour',
            field=models.CharField(default=b'#008CBA', max_length=7),
        ),
        migrations.AddField(
            model_name='happeningsite',
            name='theme_colour',
            field=models.CharField(default=b'#65afdc', max_length=7),
        ),
    ]
