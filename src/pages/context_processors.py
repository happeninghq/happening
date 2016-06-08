"""Pages context processors."""
from pages.models import Page


def pages(request):
    """Add the pages to the context."""
    pages = Page.objects.all()
    # TODO: Make this generic
    pages = [p for p in pages if not p.url == "index"]
    return {"pages": pages}
