# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20150429_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPreset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('value', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
