""" Template tags relating to plugins. """

from django import template

register = template.Library()


@register.simple_tag
def plugin_block(key, *params):
    """ Make a space for plugins to place content in a template. """
    from happening import plugins
    return " ".join([p(*params) for plugin_id, p in
                    plugins.plugin_blocks.get(key, [])
                    if plugins.plugin_enabled(plugin_id)])
