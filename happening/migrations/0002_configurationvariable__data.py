# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0001_squashed_0008_auto_20150509_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='configurationvariable',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
            preserve_default=True,
        ),
    ]
