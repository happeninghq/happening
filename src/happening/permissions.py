"""Register permissions."""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from happening.models import HappeningSite

_registered_permissions = {}


def register_permission(category, key, name, description="", model=None):
    """Register a new permission."""
    if model is None:
        model = HappeningSite
    content_type = ContentType.objects.get_for_model(model)

    if category not in _registered_permissions:
        _registered_permissions[category] = {}
    _registered_permissions[category][key] = {
        "content_type": content_type,
        "name": name,
        "description": description
    }

    permission, c = Permission.objects.get_or_create(
        content_type=content_type, codename=key,
        defaults={"name": name})
    if not c:
        permission.name = name
        permission.save()


def get_permission(category, key):
    """Turn a category and key into a Permission object."""
    content_type = _registered_permissions[category][key]["content_type"]
    return Permission.objects.get(content_type=content_type, codename=key)


register_permission(
    "Happening",
    "configuration",
    "Configure Happening",
    "Can access configuration, plugins, authentication, etc.")

register_permission(
    "Happening",
    "appearance",
    "Appearance Settings",
    "Can access Appearence, Menus, Pages, etc.")


register_permission(
    "Happening",
    "backup",
    "Backup",
    "Can manage backups.")

register_permission(
    "Happening",
    "manage_members",
    "Manage Members",
    "Can manage members.")

register_permission(
    "Happening",
    "manage_groups",
    "Manage Groups",
    "Can manage groups.")

register_permission(
    "Happening",
    "manage_events",
    "Manage Events",
    "Can manage events.")

register_permission(
    "Happening",
    "manage_emails",
    "Manage Emails",
    "Can send emails.")
