"""Site wide context processors."""
from django.conf import settings


def site_settings(request):
    """Add settings for the current site."""
    # TODO: Make this do more than just convert the django
    # settings into a dict
    return {"SITE_SETTINGS":
            {
                "SITE_TITLE": settings.SITE_TITLE
            }}
