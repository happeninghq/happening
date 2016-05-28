# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHandler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('description', models.CharField(max_length=255)),
                ('public_key', models.CharField(max_length=255)),
                ('secret_key', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
