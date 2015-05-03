"""Admin context processors."""
import importlib
from django.conf import settings

cached_admin_urls = [
    (None, "Dashboard", "admin"),
    (None, "Plugins", "plugins"),
    (None, "Configuration", "configuration"),
]


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
