"""Happening custom form elements."""
from django import forms
from django.template.loader import render_to_string
from happening.utils import convert_to_underscore
import json
from django.core.files import File
from happening.storage import storage
from datetime import timedelta


class PropertiesWidget(forms.Widget):

    """A widget that allows for configuring a list of property types."""

    def __init__(self, *args, **kwargs):
        """Create a properties widget."""
        if 'property_types' in kwargs:
            self.property_types = kwargs.pop('property_types')
        else:
            # TODO: Don't  hardcode these types
            self.property_types = (
                ("CharField", "Text"),
                ("EmailField", "Email"),
                ("IntegerField", "Number"),
                ("URLField", "URL"),
                ("BooleanField", "Boolean")
            )
        super(PropertiesWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        return render_to_string("forms/widgets/properties_widget.html", {
            "name": name,
            "value": json.dumps(value),
            "property_types": self.property_types
        })

    def value_from_datadict(self, data, files, name):
        """Get the value as a string."""
        return data[name]


class PropertiesField(forms.CharField):

    """A field that allows for configuring a list of property types."""

    widget = PropertiesWidget

    def clean(self, value):
        """Turn the JSON into a Python list."""
        return json.loads(value)


class CustomPropertiesWidget(forms.Widget):

    """A widget that allows for inputting a list of properties."""

    hide_label = True

    def __init__(self, *args, **kwargs):
        """Create a properties widget."""
        self.fields = kwargs.pop("fields")
        super(CustomPropertiesWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        # Create a form representing the fields
        if not value:
            value = {}
        if type(value) == str:
            # When the form reloads we need to turn it back into a dict
            value = json.loads(value)
        form = forms.Form()
        for field in self.fields:
            n = convert_to_underscore(field['name'])
            form.fields[name + "_" + n] = getattr(forms, field['type'])(
                label=field['name'], initial=value.get(n))

        return render_to_string(
            "forms/widgets/custom_properties_widget.html",
            {"form": form})

    def value_from_datadict(self, data, files, name):
        """Get the value as a string."""
        store_data = {}
        for k in list(data.keys()):
            if k.startswith(name + "_"):
                store_data[k[len(name) + 1:]] = data[k]
        return json.dumps(store_data)


class CustomPropertiesField(forms.CharField):

    """A field that allows for inputting multiple custom properties."""

    widget = CustomPropertiesWidget

    def __init__(self, *args, **kwargs):
        """Create the Custom Properties Field."""
        # Remove the overall label, as we want the inputs to look native
        kwargs['widget'] = self.widget(fields=kwargs.pop('fields'))
        super(CustomPropertiesField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """Turn the JSON into a Python list."""
        return json.loads(value)


class MarkdownWidget(forms.Textarea):

    """A widget that uses Quill."""

    def render(self, name, value, attrs):
        """Render the widget."""
        # attrs['class'] = 'markdown-widget ' + attrs.get('class', '')
        # Safari freezes if there's a lot of data inside an input
        # (e.g. if the user uploads an image using a data: url)
        # so instead we use a div and set up a hidden field on the other
        # side
        # return super(MarkdownWidget, self).render(name, value, attrs)
        return render_to_string(
            "forms/widgets/markdown_widget.html",
            {"name": name, "value": value, "attrs": attrs})


class MarkdownField(forms.CharField):

    """A field that uses a Quill markdown editor."""

    widget = MarkdownWidget


class DateTimeWidget(forms.TextInput):

    """A widget that adds a DateTime Picker."""

    def render(self, name, value, attrs):
        """Render the widget."""
        attrs['class'] = 'datetime-widget ' + attrs.get('class', '')
        attrs['data-datetime-format'] = 'Y-m-d H:i:00'
        return super(DateTimeWidget, self).render(name, value, attrs)


class DateWidget(forms.TextInput):

    """A widget that adds a Date Picker."""

    def render(self, name, value, attrs):
        """Render the widget."""
        attrs['class'] = 'date-widget ' + attrs.get('class', '')
        attrs['data-date-format'] = 'Y-m-d'
        return super(DateWidget, self).render(name, value, attrs)


class TitleWidget(forms.TextInput):

    """A text widget that renders a property of the instance."""

    def __init__(self, *args, **kwargs):
        """Create a TitleWidget."""
        self.model = kwargs.pop("model")
        self.field = kwargs.pop("field")
        super(TitleWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        if value:
            try:
                value = self.model.objects.get(pk=value)
                value = getattr(value, self.field)
            except:
                # If it's a form resubmission - just use the value as is
                pass
        return super(TitleWidget, self).render(name, value, attrs)


class TitleField(forms.CharField):

    """An input for an image file."""

    widget = TitleWidget

    def __init__(self, *args, **kwargs):
        """Create a TitleField."""
        self.model = kwargs.pop("model")
        self.field = kwargs.pop("field")
        self.widget = TitleWidget(model=self.model, field=self.field)
        super(TitleField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """Return the value as an object of type model."""
        return self.model.objects.get_or_create(**{self.field: value})[0]


class TimeWidget(forms.TextInput):

    """A widget that adds a time Picker."""

    def render(self, name, value, attrs):
        """Render the widget."""
        attrs['class'] = 'time-widget ' + attrs.get('class', '')
        attrs['data-time-format'] = 'H:i'
        return super(DateWidget, self).render(name, value, attrs)


class ImageWidget(forms.TextInput):

    """A widget that adds an ajax image uploader."""

    def render(self, name, value, attrs):
        """Render the widget."""
        # At this point we check if the file exists - if not we clear
        # the file
        if value:
            try:
                value.size
            except OSError:
                # The file does not exist
                value = None
            except AttributeError:
                value = None

        return render_to_string("forms/widgets/image_widget.html", {
            "name": name,
            "value": value
        })


class ImageField(forms.ImageField):

    """An input for an image file."""

    widget = ImageWidget

    def to_python(self, value):
        """Get the image selected."""
        # This just needs to return a File

        # We force this here so that a "None" value isn't an error
        self.required = False

        if not value or value == "None":
            return None

        is_temp = False
        if value.startswith("tmp"):
            is_temp = True

        # TODO: What happens if they use ../../ etc.
        # Can they mess with stuff they shouldn't?

        # TODO: Rename the file to remove the prefix
        filename = value.rsplit("/", 1)[-1]
        if is_temp:
            filename = filename.split("_", 1)[1]

        return File(storage.open(value))

    def clean(self, value, initial):
        """Turn the JSON into a Python list."""
        self.required = False
        return value


class EmailsWidget(forms.Widget):

    """A widget that allows for configuring emails."""

    def __init__(self, *args, **kwargs):
        """Create an emails widget."""
        super(EmailsWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        from events.models import Event
        if not value:
            value = []
        if not isinstance(value, str):
            value = json.dumps(value)
        return render_to_string("forms/widgets/emails_widget.html", {
            "name": name,
            "value": value,
            "events": Event.objects.all()
        })

    def value_from_datadict(self, data, files, name):
        """Get the value as a string."""
        if name in data:
            return data[name]
        return ''


class EmailsField(forms.CharField):

    """A field that allows for configuring emails."""

    widget = EmailsWidget

    def clean(self, value):
        """Turn the JSON into a Python list."""
        try:
            return json.loads(value)
        except ValueError:
            return []


class CheckboxInput(forms.widgets.CheckboxInput):

    """A checkbox which wraps the label."""

    hide_label = True

    def __init__(self, *args, **kwargs):
        """Create a CheckboxInput."""
        self.label = kwargs.pop('label')
        self.field = kwargs.pop('field')
        super(CheckboxInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        """Render the CheckboxInput."""
        return render_to_string("forms/widgets/checkbox_input.html", {
            "label": self.label,
            "field": self.field,
            "rendered_checkbox": super(CheckboxInput, self).render(
                name, value, attrs)
        })


class BooleanField(forms.BooleanField):

    """BooleanField with correct widget for Happening."""

    widget = CheckboxInput

    def __init__(self, *args, **kwargs):
        """Create the Boolean Field."""
        kwargs['widget'] = self.widget(label=kwargs.get('label', ''),
                                       field=self)
        super(BooleanField, self).__init__(*args, **kwargs)


class AddressWidget(forms.Widget):

    """A widget that allows for inputting an address."""

    def __init__(self, *args, **kwargs):
        """Create an address widget."""
        super(AddressWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        if not value:
            value = {}
        if isinstance(value, str):
            value = json.loads(value)
        return render_to_string("forms/widgets/address_widget.html", {
            "name": name,
            "value": value
        })

    def value_from_datadict(self, data, files, name):
        """Get the value as a dict."""
        return json.loads(data[name])


class EmptyWidget(forms.Widget):

    """A widget which does not render to the page."""

    hide_label = True

    def render(self, name, value, attrs):
        """Render nothing."""
        return ""


class AddressField(forms.CharField):

    """A field for inputting an address."""

    widget = AddressWidget

    def to_python(self, value):
        """Get the address as dict."""
        # This just needs to return the value
        return value


class EnabledDisabledWidget(forms.Widget):

    """A field which wrapping a field allowing it to be disabled entirely."""

    hide_label = True

    def __init__(self, *args, **kwargs):
        """Create an enableddisabled widget."""
        self.field_name = kwargs.pop("field_name")
        self.form = kwargs.pop("form")
        self.field = kwargs.pop("field")
        self.is_enabled = kwargs.pop("is_enabled")
        super(EnabledDisabledWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        field_value = self.field.initial

        if hasattr(self.form, "cleaned_data"):
            field_value = self.form.cleaned_data.get(self.field_name,
                                                     field_value)

        return render_to_string("forms/widgets/enableddisabled_widget.html", {
            "name": name,
            "value": value,
            "field": self.field,
            "field_name": self.field_name,
            "field_value": field_value,
            "is_enabled": self.is_enabled
        })


class EnabledDisabledField(forms.BooleanField):

    """A field that wraps another field and allows it to be disabled."""

    widget = EnabledDisabledWidget

    def __init__(self, *args, **kwargs):
        """Create an EnabledDisabledField."""
        self.field_name = kwargs.pop("field_name")
        self.form = kwargs.pop("form")
        self.field = kwargs.pop("field")
        self.is_enabled = kwargs.pop("is_enabled")
        self.widget = self.widget(form=self.form, field=self.field,
                                  field_name=self.field_name,
                                  is_enabled=self.is_enabled)

        kwargs["required"] = False
        super(EnabledDisabledField, self).__init__(*args, **kwargs)


class DurationWidget(forms.Widget):

    """A widget that allows for inputting a duration."""

    def render(self, name, value, attrs):
        """Render the widget."""
        if not value:
            value = 0
        if isinstance(value, timedelta):
            value = value.total_seconds()
        return render_to_string("forms/widgets/duration_widget.html", {
            "name": name,
            "value": value
        })


class DurationField(forms.CharField):

    """A field for inputting a duration (timedelta)."""

    widget = DurationWidget

    def to_python(self, value):
        """Get the duration as timedelta."""
        return timedelta(seconds=float(value))


class CurrencyWidget(forms.TextInput):

    """A widget for inputing currency."""

    def render(self, name, value, attrs):
        """Render the widget."""
        attrs['type'] = 'number'
        attrs['step'] = '0.01'
        return super(CurrencyWidget, self).render(name, value, attrs)


class DateTimeRangeWidget(forms.TextInput):

    """A widget for inputing a range."""

    hide_label = True

    def __init__(self, *args, allow_instant=False, **kwargs):
        """Create widget."""
        self.allow_instant = allow_instant
        super(DateTimeRangeWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        if not value:
            value = ""
        return render_to_string("forms/widgets/datetimerange_widget.html", {
            "name": name,
            "value": value,
            "allow-instant": self.allow_instant
        })


class DateTimeRangeField(forms.CharField):

    """A field for inputting a range."""

    widget = DateTimeRangeWidget

    def __init__(self, *args, allow_instant=False, **kwargs):
        """Create a DateTimeRangeField."""
        kwargs['widget'] = self.widget(allow_instant=allow_instant)
        kwargs["required"] = False
        super(DateTimeRangeField, self).__init__(*args, **kwargs)


class EmailToField(forms.CharField):

    """A field for targetting emails."""

    pass


class PostfixWidget(forms.TextInput):

    """A widget that postfixes some text."""

    def __init__(self, *args, **kwargs):
        """Init widget."""
        self.postfix = kwargs.pop("postfix")
        super(PostfixWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        attrs['class'] = 'postfix-widget ' + attrs.get('class', '')
        attrs['data-postfix'] = self.postfix
        return super(PostfixWidget, self).render(name, value, attrs)


class PostfixField(forms.CharField):

    """A field that postfixes some text."""

    widget = PostfixWidget

    def __init__(self, *args, **kwargs):
        """Init field."""
        kwargs['widget'] = self.widget(postfix=kwargs.pop('postfix'))
        super(PostfixField, self).__init__(*args, **kwargs)
