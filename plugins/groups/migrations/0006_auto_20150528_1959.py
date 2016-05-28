# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_remove_group_github_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketingroup',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
            preserve_default=True,
        ),
    ]
