"""Custom configuration variables."""
from happening.utils import convert_to_underscore, get_all_subclasses
from django import forms
from happening.plugins import plugin_enabled, load_file_in_plugins
from happening.forms import PropertiesField as PropertiesFormField
from happening.forms import EmailsField as EmailsFormField
from happening.forms import CustomPropertiesField as CustomPropertiesFormField
from happening.forms import BooleanField
from happening.forms import DurationField
from happening.templatetags.plugins import get_configuration
from markdown import markdown
from django.utils.html import mark_safe
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import json
from django.utils import timezone
from datetime import timedelta
from happening.forms import EnabledDisabledField, EmptyWidget
from django.forms.forms import pretty_name
from rest_framework import serializers


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


def attach_to_serializer(serializer, variable):
    """Attach configuration variables to a serializer."""
    if hasattr(variable, "__getitem__"):
        for x in variable:
            attach_to_serializer(serializer, x)
    else:
        variable.attach_to_serializer(serializer)
    return serializer


def attach_to_form(form, variable, editing=False):
    """Attach configuration variables to a form."""
    if hasattr(variable, "__getitem__"):
        for x in variable:
            attach_to_form(form, x, editing)
    else:
        if variable.settable and (not editing or variable.editable):
            variable.attach_to_form(form)
    return form


def save_variables(form, variables):
    """Save variables in a form."""
    for variable in variables:
        v = convert_to_underscore(variable.__class__.__name__)
        variable.set(form.cleaned_data.get(v))

        if variable.can_be_disabled:
            variable.set_enabled(form.cleaned_data.get(v + "__enabled"))


class Renderer(object):

    """Convert a variable value into a given data type."""

    def render(self, value):
        """Convert a variable value into a given data type."""
        return value


class MarkdownRenderer(Renderer):

    """Render the markdown in a string."""

    def render(self, value):
        """Render the markdown in a string."""
        return mark_safe(markdown(value))


class StorageMapper(object):

    """Prepare a datatype for storage."""

    def to_json(self, value):
        """Don't change value."""
        return value

    def to_python(self, value):
        """Don't change value."""
        return value


class IntStorageMapper(StorageMapper):

    """Store an int."""

    def to_python(self, value):
        """Parse to int."""
        return int(value)


class JSONStorageMapper(StorageMapper):

    """Store a dict as json."""

    def to_json(self, value):
        """Dump to json."""
        return json.dumps(value)

    def to_python(self, value):
        """Load json."""
        if not isinstance(value, str):
            # Depending on the storage, sometimes it'll come out as
            # already loaded
            return value
        try:
            return json.loads(value)
        except:
            return []


class DurationStorageMapper(StorageMapper):

    """Store a timedelta as json."""

    def to_json(self, value):
        """Dump to json."""
        return value.total_seconds()

    def to_python(self, value):
        """Load into timedelta."""
        return timedelta(seconds=float(value))


class ConfigurationVariable(object):

    """A configuration variable.

    Either for the overall system or for a model.
    """

    category = "Happening"
    default = ""
    object = None
    references = {}
    field = forms.CharField
    api_field = serializers.CharField
    required = False
    renderer = Renderer()
    storage_mapper = StorageMapper()
    label = None

    can_be_disabled = False
    default_enabled = True

    # Will this field appear on the CREATE page
    settable = True

    # Will this field also appear on the EDIT page
    editable = True

    def __init__(self, object=None, references=None):
        """Initialise the configuration for the given object."""
        if not references:
            references = {}
        self.object = object
        self.references = references

        if not self.label:
            self.label = pretty_name(convert_to_underscore(
                self.__class__.__name__))

    @property
    def fresh_object(self):
        """Return the latest version of the object."""
        if self.object:
            if isinstance(self.object, User):
                return self.object.profile
            return self.object.__class__.objects.get(pk=self.object.pk)
        return Site.objects.first().happening_site

    def django_field(self):
        """Get a form field representing this variable."""
        return self._construct_field()

    def rest_framework_field(self):
        """Get a rest framework field representing this variable."""
        f = self._construct_api_field()

        def get_attribute(attrs):
            return "LOL"
            # return attrs._data.get(instance.field_name, None)
        f.get_attribute = get_attribute
        return f

    def _construct_field(self, *args, **kwargs):
        """Create the form field representing this variable."""
        k = {
            "initial": self.get(),
            "required": self.required,
            "label": self.label}
        k.update(kwargs)
        f = self.field(*args, **k)

        # This isn't a nice way of assigning the tooltip, but as we don't
        # control all field types - it'll do for now
        f.tooltip = self.__doc__
        f.category = self.category
        return f

    def _construct_api_field(self, *args, **kwargs):
        """Create the api field representing this variable."""
        k = {
            "initial": self.get(),
            "required": self.required,
            "label": self.label}
        k.update(kwargs)
        return self.api_field(*args, **k)

    @property
    def key(self):
        """Get the underscore separated name of this configuration variable."""
        return convert_to_underscore(self.__class__.__name__)

    def get(self):
        """Get the value of this variable."""
        v = self.fresh_object._data.get(self.key)

        if v is None:
            return self.default
        return self.storage_mapper.to_python(v)

    def render(self):
        """Get the value of this variable, prepared for output in HTML."""
        return self.renderer.render(self.get())

    def is_enabled(self):
        """True if field is enabled."""
        v = None
        if self.can_be_disabled:
            v = self.fresh_object._data.get(self.key + "__enabled")

        if v is None:
            return self.default_enabled
        return v

    def set(self, value):
        """Set the value of this variable."""
        obj = self.fresh_object
        obj._data[self.key] = self.storage_mapper.to_json(value)
        obj.save()

    def set_enabled(self, value):
        """Set if this variable is enabled."""
        obj = self.fresh_object
        obj._data[self.key + "__enabled"] = value
        obj.save()

    def attach_to_form(self, form):
        """Attach this field to a form."""
        form.fields[convert_to_underscore(
            self.__class__.__name__)] = self.django_field()
        if self.can_be_disabled:
            # We need to attach a blanked version of the field, and the
            # actual field wrapped by an EnabledDisabledWidget
            form.fields[convert_to_underscore(
                self.__class__.__name__) + "__enabled"] = EnabledDisabledField(
                field_name=convert_to_underscore(self.__class__.__name__),
                form=form,
                field=self.django_field(),
                is_enabled=self.is_enabled())
            form.fields[convert_to_underscore(
                self.__class__.__name__)].widget = EmptyWidget()

    def attach_to_serializer(self, serializer):
        """Attach this field to a serializer."""
        serializer.fields[convert_to_underscore(
            self.__class__.__name__)] = self.rest_framework_field()
        if self.can_be_disabled:
            # Attach the __enabled variable
            enabled_disabled_field = serializers.BooleanField()

            def get_attribute(attrs):
                return "LOL"
                # return attrs._data.get(instance.field_name, None)
            enabled_disabled_field.get_attribute = get_attribute
            serializer.fields[convert_to_underscore(
                self.__class__.__name__) +
                "__enabled"] = enabled_disabled_field


class CharField(ConfigurationVariable):

    """A text field."""

    pass


class DurationField(CharField):

    """A duration field."""

    field = DurationField
    storage_mapper = DurationStorageMapper()


class EmailField(CharField):

    """A validated email address field."""

    field = forms.EmailField


class IntegerField(CharField):

    """An integer field."""

    field = forms.IntegerField
    storage_mapper = IntStorageMapper()


class URLField(CharField):

    """A url field."""

    field = forms.URLField


class BooleanField(ConfigurationVariable):

    """A boolean field."""

    field = BooleanField
    required = False


class ChoiceField(ConfigurationVariable):

    """A multiple choice field."""

    field = forms.ChoiceField

    def django_field(self):
        """Get a form field representing this variable."""
        return self._construct_field(choices=self.choices)


class PropertiesField(ConfigurationVariable):

    """A field to configure custom properties and types."""

    field = PropertiesFormField
    storage_mapper = JSONStorageMapper()


class EmailsField(ConfigurationVariable):

    """A field to configure emails."""

    field = EmailsFormField
    storage_mapper = JSONStorageMapper()

    def set(self, value):
        """Save this variable and then schedule the emails."""
        super(EmailsField, self).set(value)

        # Schedule emails
        if value:
            for email in value:
                self.schedule_email(email)

    def schedule_email(self, email):
        """Schedule sending this email to a given address."""
        def get_time(event, time):
            if time['start'] == 'after event creation':
                start_date = timezone.now()
            elif time['start'] == 'after event':
                start_date = event.end
                if not start_date:
                    start_date = event.start
            else:
                # Must be "before event"
                start_date = event.start

            # Now manipulate start_date appropriately
            if time['type'] == 'hours':
                offset = timedelta(hours=int(time['number']))
            elif email['start_sending']['type'] == 'days':
                offset = timedelta(days=int(time['number']))
            else:
                # Must be weeks
                offset = timedelta(weeks=int(time['number']))

            if time['start'].startswith("after"):
                return start_date + offset
            return start_date - offset

        event = self.fresh_object

        start_sending = get_time(event, email['start_sending'])
        stop_sending = get_time(event, email['stop_sending'])

        from emails.models import Email

        Email(event=event,
              to=email['to'],
              subject=email['subject'],
              content=email['content'],
              start_sending=start_sending,
              stop_sending=stop_sending).save()


class CustomProperties(ConfigurationVariable):

    """A field to hold the values for custom properties."""

    field = CustomPropertiesFormField
    storage_mapper = JSONStorageMapper()

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
        return self._construct_field(fields=t)
