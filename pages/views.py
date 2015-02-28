""" Pages views. """
from django.shortcuts import render, get_object_or_404
from models import Page


def view(request, pk):
    """ Show page. """
    page = get_object_or_404(Page, url=pk)
    return render(request, "pages/view.html", {"page": page})
