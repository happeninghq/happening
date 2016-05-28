# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pluginsetting',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
            preserve_default=True,
        ),
    ]
