"""Profile form."""

from django import forms


class PaymentForm(forms.Form):
    """Form for submitting the credit card details for payment."""

    stripe_token = forms.CharField()
