"""Admin context processors."""
import importlib
from django.conf import settings

cached_admin_urls = [
    (None, "Dashboard", "admin"),
    (None, "Plugins", "plugins"),
    (None, "Configuration", "configuration"),
    (None, "Appearance", "appearance"),
    (None, "Menus", "menus"),
    (None, "Backup", "backup"),
    (None, "Members", "staff_members"),
    (None, "Events", "staff_events"),
    (None, "Pages", "staff_pages"),
    (None, "Emails", "staff_emails"),
    (None, "Tags", "tags"),
    (None, "Tracking Links", "tracking_links")
]

if hasattr(settings, "PLUGINS"):
    for plugin in settings.PLUGINS:
        p = importlib.import_module(plugin)
        if hasattr(p, "admin") and hasattr(p.admin, "admin_links"):
            cached_admin_urls += [
                (plugin, l[0], l[1]) for l in p.admin.admin_links]


def admin_urls(request):
    """Return cached admin urls."""
    from happening import plugins
    return {"admin_urls": [
        # l[0] is for hardcoding
        (l[1], l[2]) for l in cached_admin_urls if l[0] is None or
        plugins.plugin_enabled(l[0])]}
