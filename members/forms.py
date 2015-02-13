# -*- coding: utf-8 -*-
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


class PaymentForm(forms.Form):

    """ Form for paying for a new membership. """

    amount = forms.ChoiceField(choices=(
                               ("10", u"£10"),
                               ("20", u"£20"),
                               ("50", u"£50"),
                               ("100", u"£100 (funds one complete dojo)"),
                               ("200", u"£200"),
                               ("500", u"£500"),
                               ("800", u"£800"),
                               ("1000", u"£1000 (funds one year of dojos)"),
                               ("other", "Other amount"),
                               ))
    other_amount = forms.IntegerField(required=False)

    def clean_other_amount(self):
        u""" Ensure other amount is at least £5. """
        if self.cleaned_data['amount'] == 'other':
            if self.cleaned_data['other_amount'] < 5:
                raise forms.ValidationError("You must pay at least £5")
        return self.cleaned_data['other_amount']

    @property
    def selected_amount(self):
        """ Get the actual amount the user wants to pay. """
        if self.cleaned_data['amount'] == 'other':
            return self.cleaned_data['other_amount']
        else:
            return int(self.cleaned_data['amount'])


class CompletePaymentForm(forms.Form):

    """ Form for submitting the credit card details for payment. """

    amount = forms.IntegerField()
    stripe_token = forms.CharField()
