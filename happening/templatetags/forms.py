"""Form helpers."""
from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.filter
def render(form):
    """Render a form."""
    o_label_suffix = form.label_suffix
    form.label_suffix = ""
    rendered = render_to_string("forms/_form.html", {"form": form})
    form.label_suffix = o_label_suffix
    return rendered


@register.simple_tag
def render_field(field, name, value):
    """Render a field."""
    return field.widget.render(name, value, {})
