# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-02 18:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_pgjson.fields
import notifications.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('template', models.CharField(max_length=200)),
                ('data', models.TextField()),
                ('sent_datetime', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('read_datetime', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, notifications.models.EmailableNotification),
        ),
        migrations.CreateModel(
            name='NotificationPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('notification', models.CharField(max_length=255)),
                ('send_notifications', models.BooleanField(default=True)),
                ('send_emails', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_preferences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
