"""Finances forms."""
from django import forms
from django.forms import ModelForm
from models import Account, Transaction, Payee, Category
from happening.forms import DateWidget, TitleField
from datetime import date
from django.template.loader import render_to_string


class InflowOutflowWidget(forms.TextInput):

    """A widget that generates an amount according to inflow/outflow."""

    def render(self, name, value, attrs):
        """Render the widget."""
        return render_to_string(
            "finances/forms/widgets/inflow_outflow_widget.html",
            {
                "name": name,
                "value": value
            })


class AccountForm(ModelForm):

    """Form for creating/editing accounts."""

    class Meta:
        model = Account
        fields = ['name', 'description']


class TransactionForm(ModelForm):

    """Form for creating/editing accounts."""

    date = forms.DateField(widget=DateWidget(), initial=date.today)
    payee = TitleField(model=Payee, field="name")
    category = TitleField(model=Category, field="name")
    memo = forms.CharField(widget=forms.Textarea(), required=False)

    amount = forms.FloatField(widget=InflowOutflowWidget(), label="")

    class Meta:
        model = Transaction
        fields = ['account', 'date', 'payee', 'memo', 'category', 'amount']
