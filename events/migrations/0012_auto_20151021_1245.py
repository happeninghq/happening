# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields
from django.conf import settings
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0011_auto_20151020_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingListSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('ticket_type', models.ForeignKey(related_name='waiting_list_subscriptions', to='events.TicketType')),
                ('user', models.ForeignKey(related_name='waiting_lists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
    ]
