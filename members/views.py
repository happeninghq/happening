"""Member views."""

from django.shortcuts import render, get_object_or_404, redirect
from events.models import Ticket
from events.forms import TicketForm
from forms import ProfileForm, ProfilePhotoForm, CroppingImageForm
from forms import UsernameForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from StringIO import StringIO
from PIL import Image
from django.core.files import File
from happening.configuration import get_configuration_variables
from happening.configuration import attach_to_form
from happening.configuration import save_variables
from members.user_profile import CustomProperties
from members.configuration import ProfileProperties
from decorators import require_editing_own_profile


@login_required
def my_tickets(request):
    """List tickets I have purchased."""
    return render(request, "members/my_tickets.html")


@login_required
def edit_ticket(request, pk):
    """Edit the quantity of tickets."""
    ticket = get_object_or_404(Ticket, pk=pk)

    if not ticket.user == request.user and not request.user.is_staff:
        raise Http404

    if not ticket.event.is_future:
        return redirect(request.GET.get("redirect_to", "my_tickets"))

    max_tickets = ticket.event.remaining_tickets + ticket.number + 1

    form = TicketForm(event=ticket.event,
                      initial={"quantity": ticket.number},
                      max_tickets=max_tickets)

    if request.method == "POST":
        form = TicketForm(request.POST,
                          event=ticket.event,
                          max_tickets=max_tickets)
        if form.is_valid():
            ticket.number = form.cleaned_data['quantity']
            ticket.save()
            return redirect(request.GET.get("redirect_to", "my_tickets"))

    return render(request, "members/edit_ticket.html",
                  {"ticket": ticket, "form": form})


@login_required
def cancel_ticket(request, pk):
    """Cancel a ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)

    if not ticket.user == request.user and not request.user.is_staff:
        raise Http404

    if not ticket.event.is_future:
        return redirect(request.GET.get("redirect_to", "my_tickets"))

    if request.method == "POST":
        ticket.cancel()
        return redirect(request.GET.get("redirect_to", "my_tickets"))

    return render(request, "members/cancel_ticket.html", {"ticket": ticket})


def view_profile(request, pk):
    """View a member's profile."""
    member = get_object_or_404(get_user_model(), pk=pk)

    profile_properties = ProfileProperties().get()
    custom_properties = CustomProperties(member).get()

    return render(request, "members/view_profile.html",
                  {"member": member,
                   "profile_properties": profile_properties,
                   "custom_properties": custom_properties})


@require_editing_own_profile
def edit_profile(request, pk):
    """Edit a member's profile."""
    member = get_object_or_404(get_user_model(), pk=pk)
    variables = get_configuration_variables("user_profile", member)
    form = ProfileForm(
        initial={
            "first_name": member.first_name,
            "last_name": member.last_name,
            "bio": member.profile.bio,
            "show_facebook_urls": member.profile.show_facebook_urls,
            "show_github_urls": member.profile.show_github_urls,
            "show_linkedin_urls": member.profile.show_linkedin_urls,
            "show_twitter_urls": member.profile.show_twitter_urls,
            "show_google_urls": member.profile.show_google_urls,
            "show_stackexchange_urls": member.profile.show_stackexchange_urls,
        })
    attach_to_form(form, variables)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        attach_to_form(form, variables)
        if form.is_valid():
            member.first_name = form.cleaned_data['first_name']
            member.last_name = form.cleaned_data['last_name']
            member.profile.bio = form.cleaned_data['bio']
            member.profile.show_facebook_urls = \
                form.cleaned_data['show_facebook_urls']
            member.profile.show_github_urls = \
                form.cleaned_data['show_github_urls']
            member.profile.show_linkedin_urls = \
                form.cleaned_data['show_linkedin_urls']
            member.profile.show_twitter_urls = \
                form.cleaned_data['show_twitter_urls']
            member.profile.show_google_urls = \
                form.cleaned_data['show_google_urls']
            member.profile.show_stackexchange_urls = \
                form.cleaned_data['show_stackexchange_urls']

            member.profile.save()
            member.save()
            save_variables(form, variables)

            return redirect("view_profile", member.pk)
        else:
            attach_to_form(form, variables)

    profile_photo_form = ProfilePhotoForm()

    return render(request, "members/edit_profile.html",
                  {"member": member,
                   "form": form,
                   "profile_photo_form": profile_photo_form})


@require_POST
@require_editing_own_profile
def upload_profile_photo(request, pk):
    """Upload a new profile photo and forward for cropping."""
    member = get_object_or_404(get_user_model(), pk=pk)
    form = ProfilePhotoForm(request.POST, request.FILES)

    if form.is_valid():
        member.profile.photo = request.FILES['photo']
        member.profile.save()
        return redirect("resize_crop_profile_photo", pk)
    return redirect("edit_profile", member.pk)


@require_editing_own_profile
def resize_crop_profile_photo(request, pk):
    """Resize and crop profile photo."""
    member = get_object_or_404(get_user_model(), pk=pk)
    if not member.profile.photo:
        return redirect("edit_profile", member.pk)
    form = CroppingImageForm()
    if request.method == "POST":
        form = CroppingImageForm(request.POST)
        if form.is_valid():
            # Crop the image to the correct size
            imagedata = StringIO(member.profile.photo.file.read())
            image = Image.open(imagedata)
            image = image.crop([int(form.cleaned_data['x1']),
                                int(form.cleaned_data['y1']),
                                int(form.cleaned_data['x2']),
                                int(form.cleaned_data['y2'])])

            im_data = StringIO()
            image.save(im_data, 'PNG')
            im_data.seek(0)
            image.close()

            member.profile.photo.save("%s.png" % member.id,
                                      File(im_data))

            return redirect("view_profile", pk)

    return render(request, "members/resize_crop_photo.html",
                  {"member": member,
                   "profile_photo": member.profile.photo,
                   "form": form})


@require_editing_own_profile
def settings(request, pk):
    """Overview settings."""
    member = get_object_or_404(get_user_model(), pk=pk)
    return render(request, "members/settings.html", {"member": member})


@require_editing_own_profile
def edit_username(request, pk):
    """Change username."""
    member = get_object_or_404(get_user_model(), pk=pk)
    form = UsernameForm(initial={"username": member.username})
    if request.method == "POST":
        form = UsernameForm(request.POST)
        if form.is_valid():
            member.username = form.cleaned_data['username']
            member.save()
            return redirect("settings", member.pk)
    return render(request, "members/edit_username.html",
                  {"member": member,
                   "form": form})
