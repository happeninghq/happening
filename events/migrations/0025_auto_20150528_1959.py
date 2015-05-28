# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_auto_20150517_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventpreset',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
            preserve_default=True,
        ),
    ]
