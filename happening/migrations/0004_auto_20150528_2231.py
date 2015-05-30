# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_configurationvariables(apps, schema_editor):
    """Migrate configurationvariables."""
    from happening.models import ConfigurationVariable
    from django.contrib.sites.models import Site
    for c in ConfigurationVariable.objects.all():
        if c.obj is None:
            c.obj = Site.objects.first().happening_site

        c.obj._data[c.key] = c.value
        c.obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0003_happeningsite'),
    ]

    operations = [
        migrations.RunPython(migrate_configurationvariables),
    ]
