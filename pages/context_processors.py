""" Pages context processors. """
from django.template.loader import render_to_string
from pages.models import Page


def pages_navigation(request):
    """ Add the pages navigation HTML to the context. """
    return {"pages_navigation": render_to_string("pages/navigation.html", {
        "path": Page.objects.as_navigation_path()
    })}
