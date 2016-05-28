# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20150528_1959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paidmembership',
            old_name='receipt_id',
            new_name='payment_id',
        ),
    ]
