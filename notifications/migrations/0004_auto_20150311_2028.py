# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20150308_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='site',
        ),
        migrations.RemoveField(
            model_name='notificationpreference',
            name='site',
        ),
    ]
