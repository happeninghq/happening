# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_squashed_0032_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='last_edited_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='purchased_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
