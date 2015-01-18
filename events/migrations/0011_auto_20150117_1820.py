# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='did_not_attend',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='group',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
