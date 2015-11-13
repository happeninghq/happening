"""Social Link forms."""

from django import forms
from models import SocialLink


class SocialLinkForm(forms.ModelForm):
    """Form for creating/editing sponsors."""

    class Meta:
        model = SocialLink
        fields = ['provider', 'url']

    provider = forms.ChoiceField(choices=(
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("github", "Github"),
        ("meetup", "Meetup"),
        ("email", "Email"),
    ))
