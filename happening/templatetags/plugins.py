"""Template tags relating to plugins."""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def plugin_block(context, key, *params):
    """Make a space for plugins to place content in a template."""
    from happening import plugins
    return " ".join([p(context['request'], *params) for plugin_id, p in
                    plugins.plugin_blocks.get(key, [])
                    if plugins.plugin_enabled(plugin_id)])
