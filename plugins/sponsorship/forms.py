"""Sponsorship forms."""

from django import forms
from models import Sponsor, SponsorTier
from happening.forms import MarkdownWidget


class SponsorForm(forms.ModelForm):

    """Form for creating/editing sponsors."""

    class Meta:
        model = Sponsor
        fields = ['name', 'description', 'url', 'logo']

    description = forms.CharField(widget=MarkdownWidget(), required=True)


class SponsorTierForm(forms.ModelForm):

    """Form for creating/editing sponsorship tiers."""

    class Meta:
        model = SponsorTier
        fields = ['name']


class EventSponsorForm(forms.Form):

    """Edit the sponsor for an event."""

    sponsor = forms.ModelChoiceField(queryset=Sponsor.objects.all())

    def __init__(self, *args, **kwargs):
        """Initialise the EventSponsorForm with an event."""
        event = kwargs.pop("event")
        super(EventSponsorForm, self).__init__(*args, **kwargs)

        self.fields['sponsor'] = forms.ModelChoiceField(
            queryset=Sponsor.objects.all().exclude(id__in=[
                s.sponsor.pk for s in event.event_sponsors.all()]))


class CommunitySponsorshipForm(forms.Form):

    """Add a community sponsorship to a sponsor."""

    tier = forms.ModelChoiceField(queryset=SponsorTier.objects.all())
