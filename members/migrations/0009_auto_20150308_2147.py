# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('members', '0008_auto_20150213_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='paidmembership',
            name='site',
            field=models.ForeignKey(default=1, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='site',
            field=models.ForeignKey(default=1, to='sites.Site'),
            preserve_default=False,
        ),
    ]
