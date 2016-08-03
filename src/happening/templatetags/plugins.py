"""Template tags relating to plugins."""

from django import template
import importlib
from django.utils.safestring import mark_safe
from happening.utils import convert_to_underscore

register = template.Library()


@register.simple_tag(takes_context=True)
def plugin_block(context, key, *params):
    """Make a space for plugins to place content in a template."""
    from happening import plugins
    return mark_safe(" ".join([p(context['request'], *params) for plugin_id,
                     p in plugins.plugin_blocks.get(key, [])
                     if plugins.plugin_enabled(plugin_id)]))


@register.filter()
def get_configuration(configuration_path, object=None):
    """Get a configuration variable.

    Configuration path should be e.g. groups.MaxNumberOfMembers.

    If there is an object for the configuration, pass this as a
    second variable
    """
    parts = configuration_path.rsplit(".", 1)
    # The final part is the variable, everything before that is the module
    p = importlib.import_module(parts[0])
    return getattr(p, parts[1])(object).render()
    raise Exception("Can not find configuration variable %s"
                    % configuration_path)


@register.filter()
def configuration_is_enabled(configuration_path, object=None):
    """Check if configuration variable is enabled.

    Configuration path should be e.g. groups.MaxNumberOfMembers.

    If there is an object for the configuration, pass this as a
    second variable
    """
    parts = configuration_path.rsplit(".", 1)
    # The final part is the variable, everything before that is the module
    p = importlib.import_module(parts[0])
    return getattr(p, parts[1])(object).is_enabled()
    raise Exception("Can not find configuration variable %s"
                    % configuration_path)


@register.filter()
def properties_as_table(configuration, properties):
    """Format properties as a table."""
    ret = []
    for p in configuration:
        k = convert_to_underscore(p['name'])
        if k in properties and properties[k]:
            if p['type'] == 'URLField':
                properties[k] = '<a href="%s">%s</a>' % (properties[k],
                                                         properties[k])
            ret.append(
                "<tr><th>%s</th><td>%s</td></tr>" % (p['name'], properties[k]))
    return mark_safe("".join(ret))


@register.filter
def theme_settings(site):
    """Output template variables in a css block."""
    styles = [
        "--%s: %s;" % (k, v["value"]) for k, v in
        list(site.get_theme_settings().items())]
    return mark_safe(
        '<style type="text/css">:root {%s}</style>' % "".join(styles))
