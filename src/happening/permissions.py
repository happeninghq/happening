"""Register permissions."""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from happening.models import HappeningSite

_registered_permissions = {}
_permissions_to_register = []


def register_permission(category, key, name, description="", model=None):
    """Register a new permission."""
    _permissions_to_register.append([category, key, name, description, model])


def do_register_permissions():
    """Finalise permission registration."""
    import sys
    if len(sys.argv) > 1 and 'migrate' in sys.argv[1]:
        return None  # Hide ourselves from Django migrations
    for category, key, name, description, model in _permissions_to_register:
        _do_register_permission(category, key, name, description, model)

    # Also ensure that both groups are activated
    from members.groups import get_members_group, get_admin_group
    get_members_group()
    get_admin_group()


def _do_register_permission(category, key, name, description, model):
    """Fully register a permission."""
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ('makemigrations', 'migrate'):
        return None  # Hide ourselves from Django migrations
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
