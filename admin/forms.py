"""Admin forms."""
from django import forms
from happening import forms as happening_forms
from payments.models import PaymentHandler
from allauth.socialaccount.models import SocialApp


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

    logo = happening_forms.ImageField()


class SocialAppForm(forms.ModelForm):
    """Form for creating/modifying social apps."""

    class Meta:
        model = SocialApp
        fields = ['provider', 'name', 'client_id', 'secret']
