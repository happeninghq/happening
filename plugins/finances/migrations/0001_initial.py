# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-23 14:31
from __future__ import unicode_literals

from django.db import migrations, models
import django_pgjson.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
