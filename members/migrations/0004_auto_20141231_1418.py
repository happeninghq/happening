# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20141231_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='show_facebook_urls',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='show_github_urls',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
