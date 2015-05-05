"""Happening custom form elements."""
from django import forms
from django.template.loader import render_to_string
from happening.utils import convert_to_underscore
import json


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

    def __init__(self, *args, **kwargs):
        """Create a properties widget."""
        self.fields = kwargs.pop("fields")
        super(CustomPropertiesWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        # Create a form representing the fields
        if not value:
            value = {}
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
        for k in data.keys():
            if k.startswith(name + "_"):
                store_data[k[len(name) + 1:]] = data[k]
        return json.dumps(store_data)


class CustomPropertiesField(forms.CharField):

    """A field that allows for inputting multiple custom properties."""

    widget = CustomPropertiesWidget

    def __init__(self, *args, **kwargs):
        """Create the Custom Properties Field."""
        # Remove the overall label, as we want the inputs to look native
        kwargs['label'] = ''
        kwargs['widget'] = self.widget(fields=kwargs.pop('fields'))
        super(CustomPropertiesField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """Turn the JSON into a Python list."""
        return json.loads(value)
