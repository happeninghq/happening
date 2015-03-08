# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20150202_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='sponsor',
        ),
    ]
