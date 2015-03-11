# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_auto_20150308_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paidmembership',
            name='site',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='site',
        ),
    ]
