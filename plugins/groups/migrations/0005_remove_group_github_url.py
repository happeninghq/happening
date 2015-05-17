# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20150426_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='github_url',
        ),
    ]
