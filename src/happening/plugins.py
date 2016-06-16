"""Plugin registration."""
import inspect
from django.conf import settings
import importlib
import os


plugin_blocks = {}
actions = {}

loaded_files = []


def init():
    """Ensure that all plugin decorators are called."""
    from django.conf import settings
    import os
    import importlib

    plugin_files = ['blocks',
                    'actions',
                    'notifications',
                    'middleware',
                    'page_blocks']

    for app in settings.INSTALLED_APPS:
        f = app.replace(".", "/")
        for p in plugin_files:
            if os.path.isfile("%s/%s.py" % (f, p)):
                importlib.import_module("%s.%s" % (app, p))


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
    # We assume anything that doesn't start with plugins. is core
    # and always enabled
    if not plugin_id.startswith('plugins.'):
        return True

    from admin.models import PluginSetting
    setting = PluginSetting.objects.filter(plugin_name=plugin_id).first()
    if not setting:
        return False

    return setting.enabled


registered_middlewares = {}


def process_request(func):
    """Register a process_request middleware."""
    parent_file_path = inspect.getouterframes(inspect.currentframe())[1][1]
    # Remove the last part(the file)
    parent_file_path = ".".join(parent_file_path.rsplit("/")[:-1])
    plugin_id = 'plugins.%s' % parent_file_path.split(".plugins.")[1]

    if plugin_id not in registered_middlewares:
        registered_middlewares[plugin_id] = []

    registered_middlewares[plugin_id].append(func)


class ResolvePluginMiddlewareMiddleware(object):

    """Resolve plugin middleware."""

    def process_request(self, request):
        """Resolve plugin middleware."""
        for plugin in list(registered_middlewares.keys()):
            if plugin_enabled(plugin):
                for r in registered_middlewares[plugin]:
                    response = r(request)
                    if response:
                        return response
