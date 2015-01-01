""" Profile form. """

from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.Form):

    """ Form for editing profile. """

    first_name = forms.CharField()
    last_name = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea(), required=False)
    show_facebook_urls = forms.BooleanField(label="Show Facebook Profiles",
                                            required=False)
    show_github_urls = forms.BooleanField(label="Show Github Profiles",
                                          required=False)
    show_linkedin_urls = forms.BooleanField(label="Show LinkedIn Profiles",
                                            required=False)
    show_twitter_urls = forms.BooleanField(label="Show Twitter Profiles",
                                           required=False)
    show_google_urls = forms.BooleanField(label="Show Google Profiles",
                                          required=False)
    show_stackexchange_urls = forms.BooleanField(
        label="Show StackExchange Profiles", required=False)


class ProfilePhotoForm(forms.Form):

    """ Form for uploading a new profile photo. """

    photo = forms.ImageField()


class CroppingImageForm(forms.Form):

    """ Form for when cropping an image. """

    x1 = forms.FloatField(widget=forms.HiddenInput)
    y1 = forms.FloatField(widget=forms.HiddenInput)
    x2 = forms.FloatField(widget=forms.HiddenInput)
    y2 = forms.FloatField(widget=forms.HiddenInput)


class UsernameForm(forms.Form):

    """ Form for changing username. """

    username = forms.CharField()

    def clean_username(self):
        """ Ensure the username is unique. """
        data = self.cleaned_data['username']
        if len(User.objects.filter(username=data)) > 0:
            # Not unique
            raise forms.ValidationError("Your username must be unique")
        return data
