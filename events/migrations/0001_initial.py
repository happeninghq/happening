# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('eventbrite_url', models.URLField()),
                ('challenge_language', models.CharField(max_length=200, null=True, blank=True)),
                ('challenge_title', models.CharField(max_length=200, null=True, blank=True)),
                ('challenge_text', models.TextField(null=True, blank=True)),
                ('solution_text', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'event_images', blank=True)),
                ('sponsor', models.ForeignKey(blank=True, to='sponsorship.Sponsor', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventSolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_name', models.CharField(max_length=200, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('github_url', models.URLField()),
                ('event', models.ForeignKey(related_name='solutions', to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
