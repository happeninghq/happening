"""Groups utilities."""
from django.contrib.auth.models import Group

MEMBERS_GROUP, _ = Group.objects.get_or_create(pk=1, defaults={
    "name": "Active Members"})
ADMIN_GROUP, _ = Group.objects.get_or_create(pk=2, defaults={
    "name": "Administrators"})
