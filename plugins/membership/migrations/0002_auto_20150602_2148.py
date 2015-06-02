# -*- coding: utf-8 -*-
"""Migrate memberships into plugin."""
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth import get_user_model
from plugins.membership.models import Membership


def migrate_memberships(apps, schema_editor):
    """Migrate memberships from members.paidmembership."""
    User = get_user_model()

    for user in User.objects.all():
        for old_membership in user.old_memberships.all():
            Membership(
                user=user,
                start_time=old_membership.start_time,
                end_time=old_membership.end_time,
                amount=old_membership.amount,
                payment_id=""
            ).save()


class Migration(migrations.Migration):

    """Migrate memberships into plugin."""

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_memberships),
    ]
