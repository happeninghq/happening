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
                    'page_blocks',
                    'navigation_items']

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

        plugin_id = file_path_to_plugin_id(parent_file_path)

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
        plugin_id = file_path_to_plugin_id(parent_file_path)

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


def file_path_to_plugin_id(file_path):
    """Convert a file path into a plugin ID."""
    # Remove the last part(the file)
    file_path = ".".join(file_path.rsplit("/")[:-1])
    if ".plugins." in file_path:
        # It is a plugin
        return 'plugins.%s' % file_path.split(".plugins.")[1]
    else:
        # It is core, don't prefix it
        return file_path.split('.src.')[1]


registered_navigation_items = {}


def register_navigation_item(key=None):
    """Register a navigation item for use in the navigation bar."""
    def register_navigation_item_inner(func):
        parent_file_path = inspect.getouterframes(inspect.currentframe())[1][1]
        plugin_id = file_path_to_plugin_id(parent_file_path)

        func_key = key

        if func_key is None:
            func_key = func.__name__

        if plugin_id not in registered_navigation_items:
            registered_navigation_items[plugin_id] = {}

        registered_navigation_items[plugin_id][func_key] = func
        return func
    return register_navigation_item_inner


def render_navigation_item(item, request, context={}):
    """Turn a navigation item string into HTML."""
    item_name = item.rsplit(".", 1)[1]
    plugin = item.rsplit(".", 1)[0]
    if plugin_enabled(plugin) and item_name in registered_navigation_items.get(
            plugin, {}):
        return registered_navigation_items[plugin][item_name](request, context)
    return ""


def render_navigation_items(context):
    """Render navigation items into a string."""
    items = ["events.events", "members.members", "notifications.notifications",
             "staff.staff", "admin.admin", "pages.sign_in"]
    return "".join([render_navigation_item(item, context["request"], context)
                   for item in items])


registered_middlewares = {}


def process_request(func):
    """Register a process_request middleware."""
    parent_file_path = inspect.getouterframes(inspect.currentframe())[1][1]
    plugin_id = file_path_to_plugin_id(parent_file_path)

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
