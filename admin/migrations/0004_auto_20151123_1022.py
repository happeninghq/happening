# -*- coding: utf-8 -*-


from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_backup'),
    ]

    operations = [
        migrations.AddField(
            model_name='backup',
            name='restore',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='backup',
            name='zip_file',
            field=models.FileField(null=True, upload_to=happening.storage.inner),
        ),
    ]
