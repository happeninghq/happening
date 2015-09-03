# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0009_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='happeningsite',
            name='primary_colour',
        ),
        migrations.RemoveField(
            model_name='happeningsite',
            name='theme_colour',
        ),
        migrations.AddField(
            model_name='happeningsite',
            name='theme_settings',
            field=django_pgjson.fields.JsonField(default={}),
        ),
    ]
