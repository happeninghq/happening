""" Event and ticket forms. """

from django import forms


class PurchaseForm(forms.Form):

    """ Form for purchasing tickets. """

    def __init__(self, *args, **kwargs):
        """ Initialise the PurchaseForm with an event. """
        event = kwargs.pop("event")
        super(PurchaseForm, self).__init__(*args, **kwargs)
        choices = [
            (str(x), str(x)) for x in range(1, event.remaining_tickets + 1)]
        self.fields['quantity'].choices = choices

    quantity = forms.ChoiceField(label='Quantity', choices=(("1", "1"),))
