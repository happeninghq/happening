# -*- coding: utf-8 -*-
"""Membership forms."""

from django import forms


class PaymentForm(forms.Form):

    """Form for paying for a new membership."""

    amount = forms.ChoiceField(choices=(
                               ("10", "£10"),
                               ("20", "£20"),
                               ("50", "£50"),
                               ("100", "£100"),
                               ("200", "£200"),
                               ("500", "£500"),
                               ("800", "£800"),
                               ("1000", "£1000"),
                               ))

    @property
    def selected_amount(self):
        """Get the actual amount the user wants to pay."""
        return int(self.cleaned_data['amount'])
