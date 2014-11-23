""" External views. """

from django.shortcuts import render


def index(request):
    """ Homepage. """
    return render(request, "index.html")
