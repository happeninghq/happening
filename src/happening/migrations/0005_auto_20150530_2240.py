# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0004_auto_20150528_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configurationvariable',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='ConfigurationVariable',
        ),
    ]
