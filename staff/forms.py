"""Staff forms."""

from django import forms
from happening.forms import DateTimeWidget
from django.utils import timezone


class EmailForm(forms.Form):

    """Form for sending emails."""

    to = forms.CharField()
    subject = forms.CharField(required=False)
    content = forms.CharField(widget=forms.Textarea)
    start_sending = forms.DateTimeField(widget=DateTimeWidget(),
                                        initial=timezone.now)
    stop_sending = forms.DateTimeField(widget=DateTimeWidget())
