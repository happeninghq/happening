# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0007_auto_20150607_1659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='happeningsite',
            old_name='large_logo',
            new_name='logo',
        ),
        migrations.RemoveField(
            model_name='happeningsite',
            name='small_logo',
        ),
    ]
