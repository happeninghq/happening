# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
import django_pgjson.fields
from django.conf import settings
import happening.db
import jsonfield.fields


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# events.migrations.0026_auto_20150608_2004
# events.migrations.0015_auto_20150202_1330
# events.migrations.0020_auto_20150425_1138

class Migration(migrations.Migration):

    replaces = [(b'events', '0001_initial'), (b'events', '0002_auto_20141125_2235'), (b'events', '0003_ticket'), (b'events', '0004_auto_20141126_1006'), (b'events', '0005_auto_20141126_1023'), (b'events', '0006_auto_20141126_1519'), (b'events', '0007_event_upcoming_notification_1_sent'), (b'events', '0008_event_upcoming_notification_2_sent'), (b'events', '0009_auto_20141231_1008'), (b'events', '0010_vote'), (b'events', '0011_auto_20150117_1820'), (b'events', '0012_auto_20150118_2004'), (b'events', '0013_auto_20150128_1612'), (b'events', '0014_eventtodo'), (b'events', '0015_auto_20150202_1330'), (b'events', '0017_auto_20150308_2018'), (b'events', '0018_auto_20150311_2028'), (b'events', '0019_event_title'), (b'events', '0020_auto_20150425_1138'), (b'events', '0021_auto_20150425_2135'), (b'events', '0022_auto_20150429_1941'), (b'events', '0023_eventpreset'), (b'events', '0024_auto_20150517_1834'), (b'events', '0025_auto_20150528_1959'), (b'events', '0026_auto_20150608_2004'), (b'events', '0027_auto_20150608_2056'), (b'events', '0028_auto_20150620_0914'), (b'events', '0029_event_image'), (b'events', '0030_event_location'), (b'events', '0031_remove_event_location'), (b'events', '0032_event_location')]

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='eventbrite_url',
        ),
        migrations.AddField(
            model_name='event',
            name='available_tickets',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(default=1)),
                ('event', models.ForeignKey(related_name='tickets', to='events.Event')),
                ('user', models.ForeignKey(related_name='tickets', to=settings.AUTH_USER_MODEL)),
                ('cancelled', models.BooleanField(default=False)),
                ('cancelled_datetime', models.DateTimeField(null=True, blank=True)),
                ('last_edited_datetime', models.DateTimeField(default=datetime.datetime(2014, 11, 26, 10, 23, 29, 653971, tzinfo=utc), auto_now=True)),
                ('purchased_datetime', models.DateTimeField(default=datetime.datetime(2014, 11, 26, 10, 23, 36, 149867, tzinfo=utc), auto_now_add=True)),
                ('did_not_attend', models.NullBooleanField()),
                ('group', models.IntegerField(null=True)),
                ('votes', jsonfield.fields.JSONField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='available_tickets',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='event',
            name='upcoming_notification_1_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='upcoming_notification_2_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=b'media/event_images', blank=True),
        ),
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
        ),
        # migrations.RunPython(
        #     code=events.migrations.0015_auto_20150202_1330.merge_tickets,
        # ),
        migrations.RemoveField(
            model_name='eventtodo',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='eventtodo',
            name='completed_by',
        ),
        migrations.RemoveField(
            model_name='eventtodo',
            name='event',
        ),
        migrations.DeleteModel(
            name='EventTodo',
        ),
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(default='Code Dojo', max_length=255),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='group',
        ),
        migrations.AddField(
            model_name='ticket',
            name='checked_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='checked_in_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.CreateModel(
            name='EventPreset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('_data', django_pgjson.fields.JsonField(default={})),
            ],
        ),
        migrations.RenameField(
            model_name='event',
            old_name='datetime',
            new_name='start',
        ),
        migrations.AddField(
            model_name='event',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
        ),
        migrations.AddField(
            model_name='ticket',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
        ),
        # migrations.RunPython(
        #     code=events.migrations.0026_auto_20150608_2004.migrate_dojo_fields,
        # ),
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
        migrations.RemoveField(
            model_name='event',
            name='upcoming_notification_1_sent',
        ),
        migrations.RemoveField(
            model_name='event',
            name='upcoming_notification_2_sent',
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=b'events'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=happening.db.AddressField(null=True),
        ),
    ]
