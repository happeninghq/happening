"""Pages context processors."""
from pages.models import Page


def pages(request):
    """Add the pages to the context."""
    return {"pages": Page.objects.all()}
