""" Sponsorship views. """
from django.shortcuts import render, get_object_or_404, redirect
from models import Sponsor
from website.utils import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import SponsorForm


def view_sponsor(request, pk):
    """ View a sponsor's profile. """
    sponsor = get_object_or_404(Sponsor, pk=pk)
    return render(request, "sponsorship/view.html",
                  {"sponsor": sponsor})


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
    return render(request, "sponsorship/staff/sponsors.html",
                  {"sponsors": sponsors})


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
    return render(request, "sponsorship/staff/edit_sponsor.html",
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
    return render(request, "sponsorship/staff/create_sponsor.html",
                  {"form": form})
