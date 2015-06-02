# -*- coding: utf-8 -*-
"""Membership forms."""

from django import forms


class PaymentForm(forms.Form):

    """Form for paying for a new membership."""

    amount = forms.ChoiceField(choices=(
                               ("10", u"£10"),
                               ("20", u"£20"),
                               ("50", u"£50"),
                               ("100", u"£100 (funds one complete dojo)"),
                               ("200", u"£200"),
                               ("500", u"£500"),
                               ("800", u"£800"),
                               ("1000", u"£1000 (funds one year of dojos)"),
                               ("other", "Other amount"),
                               ))
    other_amount = forms.IntegerField(required=False)

    def clean_other_amount(self):
        u"""Ensure other amount is at least £5."""
        if self.cleaned_data['amount'] == 'other':
            if self.cleaned_data['other_amount'] < 5:
                raise forms.ValidationError("You must pay at least £5")
        return self.cleaned_data['other_amount']

    @property
    def selected_amount(self):
        """Get the actual amount the user wants to pay."""
        if self.cleaned_data['amount'] == 'other':
            return self.cleaned_data['other_amount']
        else:
            return int(self.cleaned_data['amount'])
