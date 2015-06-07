"""General context processors."""
from django.contrib.sites.models import Site


def site(request):
    """Return happening site."""
    return {"site": Site.objects.first().happening_site}
