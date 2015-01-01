""" Staff views. """
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.auth.models import User
from sponsorship.models import Sponsor
from events.models import Event
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@staff_member_required
def index(request):
    """ Show the staff index. """
    return render(request, "staff/index.html")


@staff_member_required
def members(request):
    """ Administrate members. """
    members = User.objects.all()
    paginator = Paginator(members, 10)

    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        members = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        members = paginator.page(paginator.num_pages)
    return render(request, "staff/members.html", {"members": members})


@staff_member_required
def sponsors(request):
    """ Administrate sponsors. """
    sponsors = Sponsor.objects.all()
    paginator = Paginator(sponsors, 10)

    page = request.GET.get('page')
    try:
        sponsors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sponsors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sponsors = paginator.page(paginator.num_pages)
    return render(request, "staff/sponsors.html", {"sponsors": sponsors})


@staff_member_required
def events(request):
    """ Administrate events. """
    events = Event.objects.all()
    paginator = Paginator(events, 10)

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
    return render(request, "staff/events.html", {"events": events})
