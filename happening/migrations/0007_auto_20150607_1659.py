# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0006_auto_20150605_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='happeningsite',
            name='large_logo',
            field=models.ImageField(null=True, upload_to=b'site'),
        ),
        migrations.AddField(
            model_name='happeningsite',
            name='small_logo',
            field=models.ImageField(null=True, upload_to=b'site'),
        ),
    ]
