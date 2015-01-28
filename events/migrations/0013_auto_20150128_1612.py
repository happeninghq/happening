# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20150118_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='event',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
        migrations.AddField(
            model_name='ticket',
            name='votes',
            field=jsonfield.fields.JSONField(null=True),
            preserve_default=True,
        ),
    ]
