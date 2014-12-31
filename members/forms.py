""" Profile form. """

from django import forms


class ProfileForm(forms.Form):

    """ Form for editing profile. """

    first_name = forms.CharField()
    last_name = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea(), required=False)


class ProfilePhotoForm(forms.Form):

    """ Form for uploading a new profile photo. """

    photo = forms.ImageField()


class CroppingImageForm(forms.Form):

    """ Form for when cropping an image. """

    x1 = forms.FloatField(widget=forms.HiddenInput)
    y1 = forms.FloatField(widget=forms.HiddenInput)
    x2 = forms.FloatField(widget=forms.HiddenInput)
    y2 = forms.FloatField(widget=forms.HiddenInput)
