# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_event_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_number', models.IntegerField(default=0)),
                ('team_name', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('github_url', models.URLField()),
                ('event', models.ForeignKey(related_name='groups', to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketInGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(related_name='tickets', to='groups.Group')),
                ('ticket', models.ForeignKey(related_name='groups', to='events.Ticket')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
