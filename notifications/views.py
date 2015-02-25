""" Notification views. """
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def list(request):
    """ List all notifications. """
    return render(request, "notifications/list.html")


@login_required()
def short(request):
    """ Return rendered list of short notifications. """
    # TODO: Replace this with a JSON request
    # and render client side
    return render(request, "notifications/short.html")


@login_required
def settings(request):
    """ Change the user's notification settings. """
    pass
