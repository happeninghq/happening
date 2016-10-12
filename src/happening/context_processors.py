"""General context processors."""
from django.contrib.sites.models import Site
from happening.plugins import render_navigation_items


def site(request):
    """Return happening site."""
    return {"happening_site": Site.objects.first().happening_site}


def navigation_items(request):
    """Return navigation items."""
    if not hasattr(request, "_rendered_navigation_items"):
        # This is so that it doesn't recursively render
        request._rendered_navigation_items = True
        request._rendered_navigation_items = render_navigation_items(request)
    return {"navigation_items": request._rendered_navigation_items}
