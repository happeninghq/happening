# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0013_auto_20150128_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventTodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('notes', models.TextField()),
                ('completed_at', models.DateTimeField(null=True)),
                ('assigned_to', models.ForeignKey(related_name='assigned_todos', to=settings.AUTH_USER_MODEL, null=True)),
                ('completed_by', models.ForeignKey(related_name='completed_todos', to=settings.AUTH_USER_MODEL, null=True)),
                ('event', models.ForeignKey(related_name='todos', to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
