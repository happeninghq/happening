# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('amount', models.IntegerField()),
                ('payment_id', models.CharField(max_length=200)),
                ('user', models.ForeignKey(related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
