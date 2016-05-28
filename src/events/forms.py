"""Event and ticket forms."""

from django import forms
from django.forms import ModelForm
from .models import Event, TicketType
from happening import forms as happening_forms
from happening.forms import DateTimeWidget
from django.template.loader import render_to_string
import json
from payments.models import PaymentHandler


class TicketForm(forms.Form):

    """Form for purchasing/editing tickets."""

    def __init__(self, *args, **kwargs):
        """Initialise the PurchaseForm with an event."""
        event = kwargs.pop("event")
        self.max_tickets = None
        if 'max_tickets' in kwargs:
            self.max_tickets = kwargs.pop("max_tickets")
        self.user = kwargs.pop("user")
        super(TicketForm, self).__init__(*args, **kwargs)

        for ticket_type in event.ticket_types.visible_to(self.user):
            if not ticket_type.purchasable_by(self.user):
                # Don't allow any tickets not purchasable
                continue
            m = ticket_type.remaining_tickets
            if self.max_tickets:
                m = min((self.max_tickets, m))
            choices = [
                (str(x), str(x)) for x in range(0, m + 1)]
            self.fields['tickets_' + str(ticket_type.pk)] = forms.ChoiceField(
                label=ticket_type.name, choices=choices, required=False)

    def clean(self):
        """Ensure that at least one ticket is chosen."""
        cleaned_data = super(TicketForm, self).clean()

        ticket_keys = [k for k in list(cleaned_data.keys())
                       if k.startswith("tickets_")]

        def get_default_zero(t):
            if cleaned_data.get(t, "") == "":
                return 0
            return int(cleaned_data[t])

        for t in ticket_keys:
            cleaned_data[t] = get_default_zero(t)

        num_tickets_ordered = sum([cleaned_data[t] for t in ticket_keys])

        if num_tickets_ordered == 0:
            raise forms.ValidationError("You must order at least one ticket")

        # Now make sure that the user hasn't ordered more than the maximum
        if self.max_tickets and num_tickets_ordered > self.max_tickets:
            raise forms.ValidationError("You have ordered too many tickets")

        return cleaned_data


class TicketsWidget(forms.Widget):

    """A widget that allows for configuring tickets."""

    def __init__(self, *args, **kwargs):
        """Allow passing of initial data."""
        self.initial = kwargs.pop('initial', None)
        super(TicketsWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        # Convert the value into JSON
        if not value and self.initial:
            value = [{"pk": t.pk,
                      "name": t.name,
                      "number": t.number,
                      "price": float(t.price) / 100.0,
                      "restriction_enabled": t.restriction_enabled,
                      "restriction_filter": t.restriction_filter,
                      "waiting_list_enabled": t.waiting_list_enabled,
                      "visible": t.visible} for t in self.initial]
        elif not value:
            value = []

        # payment is enabled if there is an active payment provider
        payment_enabled = PaymentHandler.objects.active() is not None

        return render_to_string("forms/widgets/tickets_widget.html", {
            "name": name,
            "value": json.dumps(value),
            "payment_enabled": payment_enabled
        })

    def value_from_datadict(self, data, files, name):
        """Get the value as a string."""
        return data.get(name, "[]")


class TicketsField(forms.CharField):

    """A field that allows for configuring tickets."""

    widget = TicketsWidget

    def __init__(self, *args, **kwargs):
        """Allow passing of initial data."""
        initial = kwargs.pop('initial', None)
        self.widget = self.widget(initial=initial)
        super(TicketsField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """Turn the JSON into a Python list of Tickets."""
        return json.loads(value)


class EventForm(ModelForm):

    """Form for creating/editing events."""

    start = forms.DateTimeField(widget=DateTimeWidget())
    end = forms.DateTimeField(widget=DateTimeWidget(), required=False)
    image = happening_forms.ImageField()
    tickets = TicketsField()

    def __init__(self, *args, **kwargs):
        """Override to deal with ticket types."""
        super(EventForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            self.fields['tickets'] = TicketsField(
                initial=kwargs['instance'].ticket_types.all())

    def save(self):
        """Override save to deal with ticket types."""
        instance = super(EventForm, self).save()

        # Now we need to merge in the correct tickets

        # First we remove any ticket types which have been removed
        current_ticket_pks = [ticket['pk'] for ticket in
                              self.cleaned_data.get('tickets', [])
                              if ticket.get('pk')]

        for ticket in instance.ticket_types.all():
            if ticket.pk not in current_ticket_pks:
                ticket.delete()

        # Then update the existing tickets, and create new ones
        for ticket in self.cleaned_data.get('tickets', []):
            ticket_type = TicketType(event=instance)

            if ticket.get('pk'):
                ticket_type = TicketType.objects.get(pk=ticket['pk'])

            ticket_type.name = ticket['name']
            ticket_type.number = ticket['number']
            ticket_type.price = float(ticket['price']) * 100
            ticket_type.visible = ticket['visible']
            ticket_type.waiting_list_enabled = ticket.get(
                'waiting_list_enabled', False)
            ticket_type.restriction_enabled = ticket.get(
                'restriction_enabled', False)
            ticket_type.restriction_filter = ticket.get('restriction_filter',
                                                        '')

            ticket_type.save()

        return instance

    class Meta:
        model = Event
        fields = ['title', 'start', 'end', 'image', 'location']
