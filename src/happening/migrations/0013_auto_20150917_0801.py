# -*- coding: utf-8 -*-


from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0012_auto_20150911_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='happeningsite',
            name='logo',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
    ]
