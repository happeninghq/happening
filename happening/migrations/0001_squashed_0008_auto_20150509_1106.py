# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# happening.migrations.0003_auto_20150309_2217

class Migration(migrations.Migration):

    replaces = [(b'happening', '0001_initial'), (b'happening', '0002_auto_20150309_2216'), (b'happening', '0003_auto_20150309_2217'), (b'happening', '0004_user_site'), (b'happening', '0005_auto_20150310_0851'), (b'happening', '0006_auto_20150503_1243'), (b'happening', '0007_auto_20150503_1252'), (b'happening', '0008_auto_20150509_1106')]

    dependencies = [
        ('contenttypes', '__first__'),
        ('auth', '0001_initial'),
        ('sites', '0001_initial'),
        ('sites', '__first__'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigurationVariable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
