""" Staff context processors. """
import importlib
from django.conf import settings

cached_staff_urls = [
    (None, "Dashboard", "staff"),
    (None, "Members", "staff_members"),
    (None, "Events", "staff_events"),
    (None, "Pages", "staff_pages"),
    (None, "Send Email", "staff_send_email"),
]


for plugin in settings.PLUGINS:
    p = importlib.import_module(plugin)
    if hasattr(p, "staff") and hasattr(p.staff, "staff_links"):
        cached_staff_urls += [(plugin, l[0], l[1]) for l in
                              p.staff.staff_links]


def staff_urls(request):
    """ Return cached staff urls. """
    from happening import plugins
    return {"staff_urls": [
        # l[0] is for hardcoding
        (l[1], l[2]) for l in cached_staff_urls if l[0] is None or
        plugins.plugin_enabled(l[0])]}
