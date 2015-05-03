"""Custom configuration variables."""
from happening.utils import convert_to_underscore
from django import forms
from models import ConfigurationVariable as variable_model
from django.contrib.contenttypes.models import ContentType


def attach_to_form(form, variable):
    """Attach configuration variables to a form."""
    if hasattr(variable, "__getitem__"):
        for x in variable:
            attach_to_form(form, x)
    else:
        form.fields[convert_to_underscore(
            variable.__class__.__name__)] = variable.field()
    return form


def save_variables(form, variables):
    """Save variables in a form."""
    for variable in variables:
        v = convert_to_underscore(variable.__class__.__name__)
        if v in form.cleaned_data:
            variable.set(form.cleaned_data[v])


class ConfigurationVariable(object):

    """A configuration variable.

    Either for the overall system or for a model.
    """

    category = "Happening"
    default = ""
    object = None

    def __init__(self, object=None):
        """Initialise the configuration for the given object."""
        self.object = object

    def field(self):
        """Get a form field representing this variable."""
        return forms.CharField(initial=self.get())

    def _get_model(self):
        """Get the database model for this variable."""
        if self.object:
            contenttype = ContentType.objects.get_for_model(
                self.object.__class__)
            v = variable_model.objects.filter(
                content_type=contenttype,
                object_id=self.object.id,
                key=convert_to_underscore(self.__class__.__name__)).first()
        else:
            v = variable_model.objects.filter(
                content_type=None,
                key=convert_to_underscore(self.__class__.__name__)).first()
        return v

    def get(self):
        """Get the value of this variable."""
        v = self._get_model()
        if not v:
            return self.default
        return v.value

    def set(self, value):
        """Set the value of this variable."""
        if self.object:
            contenttype = ContentType.objects.get_for_model(
                self.object.__class__)
            v = variable_model.objects.get_or_create(
                content_type=contenttype,
                object_id=self.object.id,
                key=convert_to_underscore(self.__class__.__name__))[0]
        else:
            v = variable_model.objects.get_or_create(
                content_type=None,
                key=convert_to_underscore(self.__class__.__name__))[0]
        v.value = value
        v.save()


class CharField(ConfigurationVariable):

    """A text field."""

    pass


class EmailField(CharField):

    """A validated email address field."""

    def field(self):
        """Get a form field representing this variable."""
        return forms.EmailField(initial=self.get())


class IntegerField(CharField):

    """An integer field."""

    def field(self):
        """Get a form field representing this variable."""
        return forms.IntegerField(initial=self.get())


class URLField(CharField):

    """A url field."""

    def field(self):
        """Get a form field representing this variable."""
        return forms.URLField(initial=self.get())


class BooleanField(ConfigurationVariable):

    """A boolean field."""

    def field(self):
        """Get a form field representing this variable."""
        return forms.BooleanField(initial=self.get())


class ChoiceField(ConfigurationVariable):

    """A multiple choice field."""

    def field(self):
        """Get a form field representing this variable."""
        return forms.ChoiceField(choices=self.choices, initial=self.get())
