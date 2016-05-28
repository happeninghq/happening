# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_squashed_0032_event_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('template', models.TextField()),
                ('start_sending', models.DateTimeField()),
                ('stop_sending', models.DateTimeField()),
                ('to', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SentEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('sent_datetime', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(related_name='sent_emails', to='emails.Email')),
                ('user', models.ForeignKey(related_name='received_emails', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='email',
            old_name='template',
            new_name='content',
        ),
        migrations.AddField(
            model_name='email',
            name='subject',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='email',
            name='event',
            field=models.ForeignKey(to='events.Event', null=True),
        ),
        migrations.AddField(
            model_name='email',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
