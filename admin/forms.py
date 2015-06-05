"""Admin forms."""
from django import forms
from payments.models import PaymentHandler
from html5.forms import widgets as html5_widgets


class ConfigurationForm(forms.Form):

    """A form to attach custom configuration variables to."""

    pass


class PaymentHandlerForm(forms.ModelForm):

    """Form for creating/modifying payment handlers."""

    class Meta:
        model = PaymentHandler
        fields = ['description', 'public_key', 'secret_key']


class ThemeForm(forms.Form):

    """Form for changing theme options."""

    theme_colour = forms.CharField(widget=html5_widgets.ColorInput)
    primary_colour = forms.CharField(widget=html5_widgets.ColorInput)
