# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0002_navigationitemconfiguration'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigationitemconfiguration',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
