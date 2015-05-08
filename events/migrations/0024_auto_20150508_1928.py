# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_eventpreset'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpreset',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventpreset',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
