""" Staff forms. """

from django import forms


class EmailForm(forms.Form):

    """ Form for sending emails. """

    content = forms.CharField(widget=forms.Textarea)
