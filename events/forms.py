""" Event and ticket forms. """

from django import forms


class TicketForm(forms.Form):

    """ Form for purchasing/editing tickets. """

    def __init__(self, *args, **kwargs):
        """ Initialise the PurchaseForm with an event. """
        event = kwargs.pop("event")
        max_tickets = event.remaining_tickets + 1
        if 'max_tickets' in kwargs:
            max_tickets = kwargs.pop("max_tickets")
        super(TicketForm, self).__init__(*args, **kwargs)

        choices = [
            (str(x), str(x)) for x in range(1, max_tickets)]
        self.fields['quantity'].choices = choices

    quantity = forms.ChoiceField(label='Quantity', choices=(("1", "1"),))