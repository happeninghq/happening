# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0013_auto_20150917_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='happeningsite',
            name='logo',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
    ]
