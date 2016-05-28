# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20150425_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='github_url',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
