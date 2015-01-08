""" Staff views. """
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from sponsorship.models import Sponsor
from events.models import Event
from events.forms import EventForm
from sponsorship.forms import SponsorForm
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
def edit_sponsor(request, pk):
    """ Edit sponsor. """
    sponsor = get_object_or_404(Sponsor, pk=pk)
    form = SponsorForm(instance=sponsor)
    if request.method == "POST":
        form = SponsorForm(request.POST, request.FILES, instance=sponsor)
        if form.is_valid():
            form.save()
            return redirect("staff_sponsors")
    return render(request, "staff/edit_sponsor.html",
                  {"sponsor": sponsor, "form": form})


@staff_member_required
def create_sponsor(request):
    """ Create sponsor. """
    form = SponsorForm()
    if request.method == "POST":
        form = SponsorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("staff_sponsors")
    return render(request, "staff/create_sponsor.html", {"form": form})


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


@staff_member_required
def edit_event(request, pk):
    """ Edit event. """
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("staff_events")
    return render(request, "staff/edit_event.html",
                  {"event": event, "form": form})


@staff_member_required
def create_event(request):
    """ Create event. """
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("staff_events")
    return render(request, "staff/create_event.html", {"form": form})