""" Staff views. """
from website.utils import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from events.models import Event
from events.forms import EventForm
from pages.models import Page
from pages.forms import PageForm
from forms import EmailForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json
from notifications.notifications import AdminEventMessageNotification
from notifications.notifications import AdminMessageNotification
from django.contrib import messages


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
def make_staff(request, pk):
    """ Make a member staff. """
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.is_staff = True
        user.save()
    return redirect("staff_members")


@staff_member_required
def make_not_staff(request, pk):
    """ Make a member not staff. """
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.is_staff = False
        user.save()
    return redirect("staff_members")


@staff_member_required
def events(request):
    """ Administrate events. """
    events = Event.objects.all().order_by('-datetime')
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
def event(request, pk):
    """ View event. """
    event = get_object_or_404(Event, pk=pk)
    return render(request, "staff/event.html", {"event": event})


@staff_member_required
def edit_event(request, pk):
    """ Edit event. """
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("staff_event", event.pk)
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


@staff_member_required
def email_event(request, pk):
    """ Send an email to attendees. """
    event = get_object_or_404(Event, pk=pk)
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            # Send email to attendees
            for user in event.attending_users():
                kwargs = {"event_name": str(event),
                          "subject": form.cleaned_data.get("subject"),
                          "message": form.cleaned_data['content']}
                n = AdminEventMessageNotification(user, **kwargs)
                n.send()
            return redirect("staff_events")
    return render(request, "staff/email_event.html",
                  {"event": event, "form": form})


@staff_member_required
def send_email(request):
    """ Send an email to all members. """
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            # Send email to members
            for user in User.objects.filter(is_active=True):
                n = AdminMessageNotification(
                    user,
                    subject=form.cleaned_data.get("subject"),
                    message=form.cleaned_data['content'])
                n.send()
            return redirect("staff_send_email")
    return render(request, "staff/send_email.html",
                  {"form": form})


@staff_member_required
def get_vote_winner(request, pk):
    """ Get an AJAX response of the winning language for an event. """
    event = get_object_or_404(Event, pk=pk)
    return HttpResponse(json.dumps({"value": event.winning_language}),
                        content_type="application/json")


@staff_member_required
def pages(request):
    """ Administrate pages. """
    pages = Page.objects.all()
    paginator = Paginator(pages, 10)

    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pages = paginator.page(paginator.num_pages)
    return render(request, "staff/pages.html", {"pages": pages})


@staff_member_required
def edit_page(request, pk):
    """ Edit page. """
    page = get_object_or_404(Page, pk=pk)
    form = PageForm(instance=page)
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect("staff_pages")
    return render(request, "staff/edit_page.html",
                  {"page": page, "form": form})


@staff_member_required
def delete_page(request, pk):
    """ Delete page. """
    # page = get_object_or_404(Page, pk=pk)
    # TODO
    return redirect("staff_pages")


@staff_member_required
def create_page(request):
    """ Create page. """
    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Page created.')
            return redirect("staff_pages")
    return render(request, "staff/create_page.html", {"form": form})
