# -*- coding: utf-8 -*-


from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20160117_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettype',
            name='waiting_list_automatic',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
    ]
