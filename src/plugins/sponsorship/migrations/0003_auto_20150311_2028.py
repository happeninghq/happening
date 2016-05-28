# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0002_auto_20150308_2144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventsponsor',
            name='site',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='site',
        ),
    ]
