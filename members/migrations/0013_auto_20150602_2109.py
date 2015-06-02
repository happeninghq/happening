# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_auto_20150601_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paidmembership',
            name='user',
            field=models.ForeignKey(related_name='old_memberships', to=settings.AUTH_USER_MODEL),
        ),
    ]
