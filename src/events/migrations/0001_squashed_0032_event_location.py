# -*- coding: utf-8 -*-


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
