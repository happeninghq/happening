# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('happening', '0005_auto_20150310_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigurationVariable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        # migrations.AlterUniqueTogether(
        #     name='user',
        #     unique_together=None,
        # ),
        # migrations.RemoveField(
        #     model_name='user',
        #     name='groups',
        # ),
        # migrations.RemoveField(
        #     model_name='user',
        #     name='site',
        # ),
        # migrations.RemoveField(
        #     model_name='user',
        #     name='user_permissions',
        # ),
        # migrations.DeleteModel(
        #     name='User',
        # ),
    ]
