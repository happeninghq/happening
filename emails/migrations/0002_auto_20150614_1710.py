# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='template',
            new_name='content',
        ),
        migrations.AddField(
            model_name='email',
            name='subject',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='email',
            name='to',
            field=models.TextField(),
        ),
    ]
