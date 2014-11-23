""" External views. """

from django.shortcuts import render


def index(request):
    """ Homepage. """
    return render(request, "index.html")


def sponsorship(request):
    """ Sponsorship information, prices, etc. """
    return render(request, "sponsorship.html")


def report_1(request):
    """ April code dojo. """
    return render(request, "reports/1.html")


def report_2(request):
    """ May code dojo. """
    return render(request, "reports/2.html")


def report_3(request):
    """ June code dojo. """
    return render(request, "reports/3.html")


def report_4(request):
    """ July code dojo. """
    return render(request, "reports/4.html")


def report_5(request):
    """ August code dojo. """
    return render(request, "reports/5.html")


def report_6(request):
    """ September code dojo. """
    return render(request, "reports/6.html")


def report_7(request):
    """ October code dojo. """
    return render(request, "reports/7.html")


def report_8(request):
    """ November code dojo. """
    return render(request, "reports/8.html")
