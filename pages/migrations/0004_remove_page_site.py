# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_page_site'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='site',
        ),
    ]
