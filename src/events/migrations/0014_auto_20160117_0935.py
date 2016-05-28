# -*- coding: utf-8 -*-


from django.db import models, migrations
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20151123_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglistsubscription',
            name='can_purchase',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='waitinglistsubscription',
            name='can_purchase_expiry',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
    ]
