"""Sponsorship forms."""

from django import forms
from models import Sponsor, SponsorTier


class SponsorForm(forms.ModelForm):

    """Form for creating/editing sponsors."""

    class Meta:
        model = Sponsor
        fields = ['name', 'description', 'url', 'logo']


class SponsorTierForm(forms.ModelForm):

    """Form for creating/editing sponsorship tiers."""

    class Meta:
        model = SponsorTier
        fields = ['name']


class EventSponsorForm(forms.Form):

    """Edit the sponsor for an event."""

    sponsor = forms.ModelChoiceField(queryset=Sponsor.objects.all(),
                                     required=False)


class CommunitySponsorshipForm(forms.Form):

    """Add a community sponsorship to a sponsor."""

    tier = forms.ModelChoiceField(queryset=SponsorTier.objects.all())
