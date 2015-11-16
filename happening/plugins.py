"""Plugin registration."""
import inspect
from django.conf import settings
import importlib
import os


plugin_blocks = {}
actions = {}

loaded_files = []
enabled_plugins_cache = None


def load_file_in_plugins(filename):
    """Ensure that the given file is imported from all plugins."""
    if filename in loaded_files:
        return
    else:
        loaded_files.append(filename)

    for app in settings.INSTALLED_APPS:
        f = app.replace(".", "/")
        if os.path.isfile("%s/%s.py" % (f, filename)):
            importlib.import_module("%s.%s" % (app, filename))


def trigger_action(key, **kwargs):
    """Trigger an action with the given key."""
    for plugin_id, p in actions.get(key, []):
        if plugin_enabled(plugin_id):
            p(**kwargs)


def action(key):
    """Register an action callback for the given key."""
    def inner_action(callback):
        # This is an ugly hack to check if the plugin is enabled..
        parent_file_path = inspect.getouterframes(
            inspect.currentframe())[1][1]
        # Remove the last part(the file)
        parent_file_path = ".".join(parent_file_path.rsplit("/")[:-1])
        plugin_id = 'plugins.%s' % parent_file_path.split(".plugins.")[1]

        if key not in actions:
            actions[key] = []
        actions[key].append((plugin_id, callback))
        return callback
    return inner_action


def plugin_block(key):
    """Register a plugin block for the given key."""
    def inner_plugin_block(callback):
        # This is an ugly hack to check if the plugin is enabled..
        parent_file_path = inspect.getouterframes(
            inspect.currentframe())[1][1]
        # Remove the last part(the file)
        parent_file_path = ".".join(parent_file_path.rsplit("/")[:-1])
        plugin_id = 'plugins.%s' % parent_file_path.split(".plugins.")[1]

        if key not in plugin_blocks:
            plugin_blocks[key] = []
        plugin_blocks[key].append((plugin_id, callback))
        return callback
    return inner_plugin_block


def plugin_enabled(plugin_id):
    """True if the plugin is enabled."""
    global enabled_plugins_cache
    if enabled_plugins_cache is None:
        # Refill the cache
        enabled_plugins_cache = {}
        from admin.models import PluginSetting
        for plugin in PluginSetting.objects.all():
            enabled_plugins_cache[plugin.plugin_name] = plugin.enabled
    return enabled_plugins_cache.get(plugin_id, False)


def every(*o_args, **o_kwargs):
    """Ensure that periodic tasks are only executed for enabled plugins."""
    def every_inner(f):
        from periodically.decorators import every as periodically_every

        def every_inner_inner(*args, **kwargs):
            # First check if this plugin is enabled, if not return
            # TODO: Pull the plugin ID (as above) from the stacktrace
            # Then, we call the original method
            return f(*args, **kwargs)
        return periodically_every(*o_args, **o_kwargs)(every_inner_inner)
    return every_inner
