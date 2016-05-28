# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_paidmembership'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paidmembership',
            old_name='expiry_time',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='paidmembership',
            old_name='time_made',
            new_name='start_time',
        ),
    ]
