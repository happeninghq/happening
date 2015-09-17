# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0007_auto_20150911_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='logo',
            field=models.ImageField(upload_to=happening.storage.inner),
        ),
    ]
