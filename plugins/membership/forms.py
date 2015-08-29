# -*- coding: utf-8 -*-
"""Membership forms."""

from django import forms


class PaymentForm(forms.Form):

    """Form for paying for a new membership."""

    amount = forms.ChoiceField(choices=(
                               ("10", u"£10"),
                               ("20", u"£20"),
                               ("50", u"£50"),
                               ("100", u"£100"),
                               ("200", u"£200"),
                               ("500", u"£500"),
                               ("800", u"£800"),
                               ("1000", u"£1000"),
                               ))

    @property
    def selected_amount(self):
        """Get the actual amount the user wants to pay."""
        return int(self.cleaned_data['amount'])
