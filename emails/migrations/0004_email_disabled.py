# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_email_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
