# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='event',
            field=models.ForeignKey(related_name='raw_groups', to='events.Event'),
            preserve_default=True,
        ),
    ]
