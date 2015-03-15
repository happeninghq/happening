"""Sponsorship forms."""

from django import forms
from models import Sponsor


class SponsorForm(forms.ModelForm):

    """Form for creating/editing sponsors."""

    class Meta:
        model = Sponsor
        fields = ['name', 'description', 'url', 'logo']


class EventSponsorForm(forms.Form):

    """Edit the sponsor for an event."""

    sponsor = forms.ModelChoiceField(queryset=Sponsor.objects.all(),
                                     required=False)
