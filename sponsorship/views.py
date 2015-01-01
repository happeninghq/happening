""" Sponsorship views. """
from django.shortcuts import render, get_object_or_404
from models import Sponsor


def view_sponsor(request, pk):
    """ View a sponsor's profile. """
    sponsor = get_object_or_404(Sponsor, pk=pk)
    return render(request, "sponsorship/view.html",
                  {"sponsor": sponsor})
