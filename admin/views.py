""" Admin views. """
from django.shortcuts import render


def index(request):
    """ Admin dashboard. """
    return render(request, "admin/index.html")
