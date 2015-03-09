""" Staff context processors. """
import importlib
from django.conf import settings

cached_staff_urls = [
    ("Dashboard", "staff"),
    ("Members", "staff_members"),
    ("Events", "staff_events"),
    ("Pages", "staff_pages"),
    ("Send Email", "staff_send_email"),
]


for plugin in settings.PLUGINS:
    p = importlib.import_module(plugin)
    if hasattr(p, "staff") and hasattr(p.staff, "staff_links"):
        cached_staff_urls += p.staff.staff_links


def staff_urls(request):
    """ Return cached staff urls. """
    return {"staff_urls": cached_staff_urls}
