"""Pages views."""
from django.shortcuts import render, get_object_or_404
from .models import Page
from .utils import render_block


def view(request, pk):
    """Show page."""
    page = get_object_or_404(Page, url=pk)

    # We can use .content directly as we're using a dictionary lookup
    # So the unused blocks won't be included
    blockLists = [[render_block(page.content["blocks"][i], request)
                   for i in l] for l in page.filtered_block_lists]

    return render(request, "pages/view.html",
                  {"page": page, "primaryblocks": blockLists[0],
                   "secondaryblocks": blockLists[1]})
