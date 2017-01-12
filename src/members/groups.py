"""Groups utilities."""
from django.contrib.auth.models import Group


def get_members_group():
    """Get the members group."""
    return Group.objects.get_or_create(pk=1, defaults={
        "name": "Active Members"})[0]


def get_admin_group():
    """Get the admin group."""
    return Group.objects.get_or_create(pk=2, defaults={
        "name": "Administrators"})[0]
