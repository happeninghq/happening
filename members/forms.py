# -*- coding: utf-8 -*-
"""Profile form."""

from django import forms
from happening import forms as happening_forms
from happening.forms import MarkdownWidget
from django.contrib.auth import get_user_model


class ProfileForm(forms.Form):
    """Form for editing profile."""

    first_name = forms.CharField()
    last_name = forms.CharField()
    bio = forms.CharField(widget=MarkdownWidget(), required=False)
    profile_image = happening_forms.ImageField()
    show_facebook_urls = happening_forms.BooleanField(
        label="Show Facebook Profiles", required=False)
    show_github_urls = happening_forms.BooleanField(
        label="Show Github Profiles", required=False)
    show_linkedin_urls = happening_forms.BooleanField(
        label="Show LinkedIn Profiles", required=False)
    show_twitter_urls = happening_forms.BooleanField(
        label="Show Twitter Profiles", required=False)
    show_google_urls = happening_forms.BooleanField(
        label="Show Google Profiles", required=False)
    show_stackexchange_urls = happening_forms.BooleanField(
        label="Show StackExchange Profiles", required=False)

    def __init__(self, *args, **kwargs):
        """Ensure we only show appropriate inputs."""
        profile = kwargs.pop("profile")
        super(ProfileForm, self).__init__(*args, **kwargs)

        for provider in [
                "facebook", "github", "linkedin", "twitter", "google",
                "stackexchange"]:
            if not profile.user.socialaccount_set.filter(
                    provider=provider).count() > 0:
                del self.fields['show_%s_urls' % provider]


class UsernameForm(forms.Form):
    """Form for changing username."""

    username = forms.CharField()

    def clean_username(self):
        """Ensure the username is unique."""
        data = self.cleaned_data['username']
        if len(get_user_model().objects.filter(username=data)) > 0:
            # Not unique
            raise forms.ValidationError("Your username must be unique")
        return data
