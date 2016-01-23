"""Finances forms."""
from django import forms
from django.forms import ModelForm
from models import Account, Transaction, Payee, Category
from happening.forms import DateWidget, CurrencyWidget
from datetime import date


class AccountForm(ModelForm):

    """Form for creating/editing accounts."""

    class Meta:
        model = Account
        fields = ['name', 'description']


class TransactionForm(ModelForm):

    """Form for creating/editing accounts."""

    date = forms.DateField(widget=DateWidget(), initial=date.today)
    payee = forms.CharField()
    category = forms.CharField()
    memo = forms.CharField(widget=forms.Textarea(), required=False)

    inflow = forms.FloatField(widget=CurrencyWidget(), required=False)
    outflow = forms.FloatField(widget=CurrencyWidget(), required=False)

    class Meta:
        model = Transaction
        fields = ['account', 'date', 'payee', 'memo', 'category']

    def clean_payee(self):
        """Convert the text to a Payee."""
        data = self.cleaned_data['payee']
        return Payee.objects.get_or_create(name=data)[0]

    def clean_category(self):
        """Convert the text to a Category."""
        data = self.cleaned_data['category']
        return Category.objects.get_or_create(name=data)[0]

    def clean_inflow(self):
        """Convert the float into an int (* 100)."""
        data = self.cleaned_data['inflow']
        if not data:
            data = 0
        return float(data) * 100

    def clean_outflow(self):
        """Ensure inflow or outflow is provided."""
        inflow = self.cleaned_data['inflow']
        data = self.cleaned_data['outflow']

        if not inflow and not data:
            raise forms.ValidationError("You must provide an inflow or" +
                                        " an outflow")

        print inflow
        print data
        if inflow > 0 and data:
            raise forms.ValidationError("You must provide only one of inflow" +
                                        " and outflow")

        if not data:
            data = 0

        return float(data) * 100
