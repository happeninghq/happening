# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0026_auto_20150608_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='challenge_language',
        ),
        migrations.RemoveField(
            model_name='event',
            name='challenge_text',
        ),
        migrations.RemoveField(
            model_name='event',
            name='challenge_title',
        ),
        migrations.RemoveField(
            model_name='event',
            name='image',
        ),
        migrations.RemoveField(
            model_name='event',
            name='solution_text',
        ),
    ]
