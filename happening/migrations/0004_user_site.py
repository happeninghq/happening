# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('happening', '0003_auto_20150309_2217'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='user',
        #     name='site',
        #     field=models.ForeignKey(default=1, to='sites.Site'),
        #     preserve_default=False,
        # ),
    ]
