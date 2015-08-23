"""Staff forms."""

from django import forms
from happening.forms import DateTimeWidget, MarkdownField
from django.utils import timezone
from emails.models import Email


class EmailForm(forms.ModelForm):

    """Form for sending emails."""

    class Meta:
        model = Email
        fields = ['to', 'subject', 'content', 'start_sending', 'stop_sending']

    to = forms.CharField(required=False)
    content = MarkdownField()
    start_sending = forms.DateTimeField(widget=DateTimeWidget(),
                                        initial=timezone.now)
    stop_sending = forms.DateTimeField(widget=DateTimeWidget())
