"""Socal Links views."""
from django.shortcuts import render, get_object_or_404, redirect
from models import SocialLink
from happening.utils import admin_required
from forms import SocialLinkForm
from django.views.decorators.http import require_POST
from django.contrib import messages


@admin_required
def social_links(request):
    """Administrate social links."""
    social_links = SocialLink.objects.all()
    return render(request, "social_links/social_links.html",
                  {"social_links": social_links})


@admin_required
def edit_social_link(request, pk):
    """Edit social link."""
    social_link = get_object_or_404(SocialLink, pk=pk)
    form = SocialLinkForm(instance=social_link)
    if request.method == "POST":
        form = SocialLinkForm(request.POST, request.FILES,
                              instance=social_link)
        if form.is_valid():
            form.save()
            return redirect("social_links")
    return render(request, "social_links/edit_social_link.html",
                  {"social_link": social_link, "form": form})


@admin_required
def create_social_link(request):
    """Create social link."""
    form = SocialLinkForm()
    if request.method == "POST":
        form = SocialLinkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("social_links")
    return render(request, "social_links/create_social_link.html",
                  {"form": form})


@admin_required
@require_POST
def delete_social_link(request, pk):
    """Delete social link."""
    social_link = get_object_or_404(SocialLink, pk=pk)
    social_link.delete()
    messages.success(request, "Social link deleted.")
    return redirect("social_links")
