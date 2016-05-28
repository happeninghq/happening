# -*- coding: utf-8 -*-


from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0006_auto_20150911_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='logo',
            field=models.ImageField(upload_to=happening.storage.inner),
        ),
    ]
