# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_configurationvariables(apps, schema_editor):
    """Migrate configurationvariables."""
    from happening.models import ConfigurationVariable
    from django.contrib.sites.models import Site
    from django.contrib.auth.models import User
    for c in ConfigurationVariable.objects.all():
        if c.content_object is None:
            c.content_object = Site.objects.first().happening_site

        if isinstance(c.content_object, User):
            c.content_object = c.content_object.profile

        c.content_object._data[c.key] = c.value
        c.content_object.save()


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0003_happeningsite'),
    ]

    operations = [
        migrations.RunPython(migrate_configurationvariables),
    ]
