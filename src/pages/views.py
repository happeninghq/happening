"""Pages views."""
from django.shortcuts import render, get_object_or_404
from .models import Page
from .utils import render_block


def view(request, pk):
    """Show page."""
    page = get_object_or_404(Page, url=pk)

    blockLists = [[render_block(page.content["blocks"][i], request)
                   for i in l] for l in page.content["blockLists"]]

    return render(request, "pages/view.html",
                  {"page": page, "primaryblocks": blockLists[0],
                   "secondaryblocks": blockLists[1]})
