# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_remove_page_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='_data',
            field=django_pgjson.fields.JsonField(default={}),
            preserve_default=True,
        ),
    ]
