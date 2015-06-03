# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_auto_20150602_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paidmembership',
            name='user',
        ),
        migrations.DeleteModel(
            name='PaidMembership',
        ),
    ]
