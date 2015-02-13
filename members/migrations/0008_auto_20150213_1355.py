# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_auto_20150213_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paidmembership',
            name='receipt',
        ),
        migrations.AddField(
            model_name='paidmembership',
            name='receipt_id',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
