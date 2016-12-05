"""Admin forms."""
from django import forms
from happening import forms as happening_forms
from payments.models import PaymentHandler
from allauth.socialaccount.models import SocialApp
from happening.models import NavigationItemConfiguration
from happening.forms import BooleanField, MarkdownField
from happening.forms import EmailToField, DateTimeRangeField
from emails.models import Email


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


class AddMenuForm(forms.ModelForm):

    """Form for adding a menu."""

    class Meta:
        model = NavigationItemConfiguration
        fields = ['name']

    def __init__(self, *args, **kwargs):
        """Initialise menu form."""
        menus = kwargs.pop("menus")
        super(AddMenuForm, self).__init__(*args, **kwargs)

        self.fields["name"] = forms.ChoiceField(choices=menus)


class EmailForm(forms.ModelForm):

    """Form for sending emails."""

    class Meta:
        model = Email
        fields = ['to', 'subject', 'content']

    to = EmailToField()
    content = MarkdownField()
    sending_range = DateTimeRangeField(allow_instant=True)

    def save(self, commit=True):
        """Save email."""
        instance = super(EmailForm, self).save(commit=commit)

        if not self.cleaned_data['sending_range'] == '':
            parts = self.cleaned_data['sending_range'].split("---")
            instance.start_sending = parts[0]
            instance.stop_sending = parts[1]

        if commit:
            instance.save()

        return instance


class WaitingListForm(forms.Form):

    """Form for setting up waiting lists."""

    automatic = BooleanField(label="Automatically manage waiting list",
                             required=False)


class PageForm(forms.Form):
    """Form for creating a page."""

    url = forms.CharField()
    title = forms.CharField()
