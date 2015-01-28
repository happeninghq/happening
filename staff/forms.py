""" Staff forms. """

from django import forms


class EmailForm(forms.Form):

    """ Form for sending emails. """

    subject = forms.CharField(required=False)
    content = forms.CharField(widget=forms.Textarea)
