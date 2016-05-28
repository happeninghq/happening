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
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('description', models.TextField()),
                ('amount', models.IntegerField()),
                ('success_url_name', models.CharField(max_length=255)),
                ('failure_url_name', models.CharField(max_length=255)),
                ('metadata', django_pgjson.fields.JsonField(default={})),
                ('extra', django_pgjson.fields.JsonField(default={})),
                ('status', models.CharField(default=b'PENDING', max_length=7)),
                ('complete', models.BooleanField(default=False)),
                ('error', models.TextField(null=True)),
                ('reciept_id', models.TextField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
