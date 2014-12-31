# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20141231_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='show_google_urls',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='show_linkedin_urls',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='show_stackexchange_urls',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='show_twitter_urls',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
