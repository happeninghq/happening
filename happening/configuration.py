"""Custom configuration variables."""
from happening.utils import convert_to_underscore, get_all_subclasses
from django import forms
from happening.plugins import plugin_enabled, load_file_in_plugins
from happening.forms import PropertiesField as PropertiesFormField
from happening.forms import CustomPropertiesField as CustomPropertiesFormField
from happening.templatetags.plugins import get_configuration
from markdown_deux import markdown
from django.utils.html import mark_safe
from django.contrib.sites.models import Site
import json


def get_configuration_variables(filename, object=None, **kwargs):
    """Get variables associated with the given filename."""
    load_file_in_plugins(filename)

    def enabled_if_plugin(c):
        """If c is a plugin, is it enabled. Otherwise True."""
        if c.__module__.startswith("plugins."):
            # Remove the .plugins to get the plugin name
            return plugin_enabled(c.__module__.rsplit(".", 1)[0])
        return True
    # We ignore the "basic types" defined in happening.configuration
    variables = [c(object, kwargs) for c in
                 get_all_subclasses(ConfigurationVariable)
                 if not c.__module__ == 'happening.configuration' and
                 c.__module__.endswith('.%s' % filename) and
                 enabled_if_plugin(c)]
    return variables


def attach_to_form(form, variable):
    """Attach configuration variables to a form."""
    if hasattr(variable, "__getitem__"):
        for x in variable:
            attach_to_form(form, x)
    else:
        form.fields[convert_to_underscore(
            variable.__class__.__name__)] = variable.django_field()
    return form


def save_variables(form, variables):
    """Save variables in a form."""
    for variable in variables:
        v = convert_to_underscore(variable.__class__.__name__)
        if v in form.cleaned_data:
            variable.set(form.cleaned_data[v])


class Renderer(object):

    """Convert a variable value into a given data type."""

    def render(self, value):
        """Convert a variable value into a given data type."""
        return value

    def to_string(self, value):
        """Convert a value into a string for storage."""
        return value


class StringRenderer(Renderer):

    """Convert a variable into a string."""

    def render(self, value):
        """Convert a variable into a string."""
        return str(value)


class IntRenderer(Renderer):

    """Convert a variable into a int."""

    def render(self, value):
        """Convert a variable into a int."""
        return int(value)


class JSONRenderer(Renderer):

    """Convert a variable from JSON into a dict."""

    def render(self, value):
        """Convert a variable from JSON into a dict."""
        # Because of the JSONField - it is already a dict
        return value

    def to_string(self, value):
        """Convert a value into a string for storage."""
        # This should automatically be stored correctly now...
        return json.dumps(value)


class MarkdownRenderer(Renderer):

    """Render the markdown in a string."""

    def render(self, value):
        """Render the markdown in a string."""
        return mark_safe(markdown(value))


class ConfigurationVariable(object):

    """A configuration variable.

    Either for the overall system or for a model.
    """

    category = "Happening"
    default = ""
    object = None
    references = {}
    renderer = StringRenderer()
    field = forms.CharField

    def __init__(self, object=None, references=None):
        """Initialise the configuration for the given object."""
        if not references:
            references = {}
        self.references = references

    @property
    def fresh_object(self):
        """Return the latest version of the object."""
        if self.object:
            return self.object.__class__.objects.get(pk=self.object.pk)
        return Site.objects.first().happening_site

    def django_field(self):
        """Get a form field representing this variable."""
        return self.field(initial=self._raw_value())

    @property
    def key(self):
        """Get the underscore separated name of this configuration variable."""
        return convert_to_underscore(self.__class__.__name__)

    def get(self):
        """Get the value of this variable."""
        return self.renderer.render(self._raw_value())

    def _raw_value(self):
        """Get the raw value of this variable."""
        return self.fresh_object._data.get(self.key, self.default)

    def set(self, value):
        """Set the value of this variable."""
        # TODO: This may cause a race condition
        obj = self.fresh_object
        obj._data[self.key] = value
        obj.save()


class CharField(ConfigurationVariable):

    """A text field."""

    pass


class EmailField(CharField):

    """A validated email address field."""

    field = forms.EmailField


class IntegerField(CharField):

    """An integer field."""

    renderer = IntRenderer()
    field = forms.IntegerField


class URLField(CharField):

    """A url field."""

    field = forms.URLField


class BooleanField(ConfigurationVariable):

    """A boolean field."""

    field = forms.BooleanField


class ChoiceField(ConfigurationVariable):

    """A multiple choice field."""

    field = forms.ChoiceField

    def django_field(self):
        """Get a form field representing this variable."""
        return self.field(choices=self.choices, initial=self.get())


class PropertiesField(ConfigurationVariable):

    """A field to configure custom properties and types."""

    renderer = JSONRenderer()
    field = PropertiesFormField

    def django_field(self):
        """Get a form field representing this variable."""
        return self.field(initial=self.get())


class CustomProperties(ConfigurationVariable):

    """A field to hold the values for custom properties."""

    renderer = JSONRenderer()
    field = CustomPropertiesFormField

    def django_field(self):
        """Get multiple form fields representing the custom properties."""
        if hasattr(self, "configuration_variable_instance"):
            if self.configuration_variable_instance in self.references:
                t = get_configuration(
                    self.configuration_variable,
                    self.references[self.configuration_variable_instance])
            else:
                raise Exception(
                    "%s not found" % self.configuration_variable_instance)
        else:
            t = get_configuration(self.configuration_variable)
        return self.field(initial=self.get(), fields=t)
