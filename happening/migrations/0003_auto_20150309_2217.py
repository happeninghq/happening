# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def migrate_users(apps, schema_editor):
    OldUser = apps.get_model("auth", "User")
    User = apps.get_model("happening", "User")
    for old_u in OldUser.objects.all():
        new_u = User.objects.create(
            date_joined=old_u.date_joined,
            email=old_u.email,
            first_name=old_u.first_name,
            id=old_u.id,
            username=old_u.username,
            is_active=old_u.is_active,
            is_staff=old_u.is_staff,
            is_superuser=old_u.is_superuser,
            last_login=old_u.last_login,
            last_name=old_u.last_name,
            password=old_u.password)
        new_u.user_permissions = old_u.user_permissions.all()
        new_u.groups = old_u.groups.all()

class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0002_auto_20150309_2216'),
    ]

    operations = [
        migrations.RunPython(migrate_users),
    ]
