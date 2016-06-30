"""Staff forms."""

from django import forms
from happening.forms import BooleanField, MarkdownField
from happening.forms import EmailToField, DateTimeRangeField
from emails.models import Email


class EmailForm(forms.ModelForm):

    """Form for sending emails."""

    class Meta:
        model = Email
        fields = ['to', 'subject', 'content']

    to = EmailToField()
    content = MarkdownField()
    sending_range = DateTimeRangeField(allow_instant=True)

    def save(self, commit=True):
        """Save email."""
        instance = super(EmailForm, self).save(commit=commit)

        if not self.cleaned_data['sending_range'] == '':
            parts = self.cleaned_data['sending_range'].split("---")
            instance.start_sending = parts[0]
            instance.stop_sending = parts[1]

        if commit:
            instance.save()

        return instance


class WaitingListForm(forms.Form):

    """Form for setting up waiting lists."""

    automatic = BooleanField(label="Automatically manage waiting list",
                             required=False)


class PageForm(forms.Form):
    """Form for creating a page."""

    url = forms.CharField()
    title = forms.CharField()
