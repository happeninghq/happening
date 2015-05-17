"""Event and ticket forms."""

from django import forms
from django.forms import ModelForm
from models import Event
from happening.forms import DateTimeWidget


class TicketForm(forms.Form):

    """Form for purchasing/editing tickets."""

    def __init__(self, *args, **kwargs):
        """Initialise the PurchaseForm with an event."""
        kwargs.pop("event")
        # max_tickets = event.remaining_tickets + 1
        if 'max_tickets' in kwargs:
            kwargs.pop("max_tickets")
        #     max_tickets = kwargs.pop("max_tickets")
        super(TicketForm, self).__init__(*args, **kwargs)

        # choices = [
        #     (str(x), str(x)) for x in range(1, max_tickets)]
        # self.fields['quantity'].choices = choices

    quantity = forms.ChoiceField(label='Quantity', choices=(("1", "1"),))


class EventForm(ModelForm):

    """Form for creating/editing events."""

    start = forms.DateTimeField(widget=DateTimeWidget())
    end = forms.DateTimeField(widget=DateTimeWidget(), required=False)

    class Meta:
        model = Event
        fields = ['title', 'start', 'end', 'available_tickets',
                  'challenge_language', 'challenge_title',
                  'challenge_text', 'solution_text', 'image']


class GroupNumberForm(forms.Form):

    """Form for members to indicate their group number if they attended."""

    group_number = forms.ChoiceField(
        [(0, "Did Not Attend")] + [(i, str(i)) for i in range(1, 10)])


class GroupSubmissionForm(forms.Form):

    """Form for members to pass the info for their group."""

    description = forms.CharField(label="Short description of attempt",
                                  required=False)
    github_url = forms.URLField(label="Code URL")
