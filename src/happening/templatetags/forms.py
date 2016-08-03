"""Form helpers."""
from django import template
from django.template.loader import render_to_string
from collections import OrderedDict

register = template.Library()


@register.filter
def render_as_blocks(form):
    """Render a form using blocks to contain sections."""
    o_label_suffix = form.label_suffix
    form.label_suffix = ""

    categories = {}

    for bf in form:
        field = bf.field
        if not hasattr(field, "category"):
            # This should deal with EnabledDisabledFields
            if hasattr(field, "field"):
                field = field.field

        category = "General"
        if hasattr(field, "category"):
            category = field.category

        if category not in categories:
            categories[category] = []
        categories[category].append(bf)

    # Sort categories alphabetically
    categories = OrderedDict(sorted(categories.items()))

    rendered = render_to_string("forms/_blocks_form.html",
                                {"categories": categories})
    form.label_suffix = o_label_suffix
    return rendered


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
