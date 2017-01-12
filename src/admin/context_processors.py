"""Admin context processors."""

cached_admin_urls = [
    (None, "Dashboard", "admin"),
    (None, "Configuration", "configuration"),
    (None, "Appearance", "appearance"),
    (None, "Members", "staff_members"),
    (None, "Events", "staff_events"),
    (None, "Emails", "staff_emails"),
    (None, "Backup", "backup"),
]

loaded_plugins = False


def admin_urls(request=None):
    """Return cached admin urls."""
    from happening import plugins
    import importlib
    from django.conf import settings

    global cached_admin_urls
    global loaded_plugins

    if not loaded_plugins:
        loaded_plugins = True
        if hasattr(settings, "PLUGINS"):
            for plugin in settings.PLUGINS:
                p = importlib.import_module(plugin)
                if hasattr(p.Plugin, "admin_url_root") and hasattr(p.admin, "admin_links"):
                    cached_admin_urls += [
                        (plugin, l[0], l[1]) for l in p.admin.admin_links]

    return {"admin_urls": [
        # l[0] is for hardcoding
        (l[1], l[2]) for l in cached_admin_urls if l[0] is None or
        plugins.plugin_enabled(l[0])]}
