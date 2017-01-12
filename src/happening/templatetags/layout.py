"""Template tags relating to layout."""

from django import template
from django.template.loader import render_to_string
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def primary_navigation_item(context, *params, **kwargs):
    """Render navigation items."""
    context["text"] = kwargs.pop("text")
    context["link_name"] = kwargs.pop("link_name")
    context["icon"] = kwargs.pop("icon")
    context["link"] = reverse(context["link_name"], kwargs=kwargs)
    return render_to_string("_primary_navigation_item.html", context)


@register.simple_tag(takes_context=True)
def secondary_navigation_item(context, *params, **kwargs):
    """Render navigation items."""
    context["text"] = kwargs.pop("text")
    context["link_name"] = kwargs.pop("link_name")
    context["link"] = reverse(context["link_name"], kwargs=kwargs)
    return render_to_string("_secondary_navigation_item.html", context)


@register.simple_tag(takes_context=True)
def tertiary_navigation_item(context, *params, **kwargs):
    """Render navigation items."""
    context["text"] = kwargs.pop("text")
    context["link_name"] = kwargs.pop("link_name")
    context["link"] = reverse(context["link_name"], kwargs=kwargs)
    return render_to_string("_tertiary_navigation_item.html", context)
