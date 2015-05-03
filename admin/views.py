"""Admin views."""
from django.shortcuts import render, redirect
from happening.utils import admin_required, get_all_subclasses
from django.conf import settings
import importlib
from django.contrib import messages
from models import PluginSetting
from happening.configuration import ConfigurationVariable, attach_to_form
from happening.configuration import save_variables
from forms import ConfigurationForm
from happening.plugins import plugin_enabled


@admin_required
def index(request):
    """Admin dashboard."""
    return render(request, "admin/index.html")


def format_plugin(plugin_id, plugin):
    """Return a single formatted plugin.

    Format is (id, name, description, enabled)
    """
    enabled = False

    preference = PluginSetting.objects.filter(plugin_name=plugin_id).first()
    if preference:
        enabled = preference.enabled

    return (plugin_id, plugin.Plugin.name, plugin.Plugin.__doc__, enabled)


def save_plugins(request, plugins):
    """Save plugin preferences to the database."""
    for plugin_id in plugins.keys():
        preference, _ = PluginSetting.objects.get_or_create(
            plugin_name=plugin_id)
        preference.enabled = False
        if plugin_id + "_plugin" in request.POST:
            preference.enabled = True
        preference.save()
    messages.success(request,
                     "Your plugin settings have been saved")
    return redirect("plugins")


@admin_required
def plugins(request):
    """Plugin settings."""
    plugins = {}

    for plugin in settings.PLUGINS:
        p = importlib.import_module(plugin)
        plugins[plugin] = p

    if request.method == "POST":
        # Save the plugins
        return save_plugins(request, plugins)

    formatted_plugins = [
        format_plugin(p_id, plugin) for p_id, plugin in plugins.items()]

    return render(request, "admin/plugins.html",
                  {"plugins": formatted_plugins})


@admin_required
def configuration(request):
    """Configure settings."""
    def enabled_if_plugin(c):
        """If c is a plugin, is it enabled. Otherwise True."""
        if c.__module__.startswith("plugins."):
            # Remove the .plugins to get the plugin name
            return plugin_enabled(c.__module__.rsplit(".", 1)[0])
        return True
    # We ignore the "basic types" defined in happening.configuration
    variables = [c() for c in get_all_subclasses(ConfigurationVariable)
                 if not c.__module__ == 'happening.configuration' and
                 c.__module__.endswith('.configuration')
                 and enabled_if_plugin(c)]

    form = ConfigurationForm()

    if request.method == "POST":
        form = ConfigurationForm(request.POST)
        attach_to_form(form, variables)
        if form.is_valid():
            save_variables(form, variables)
            messages.success(request, "Configuration updated.")
            return redirect("configuration")
    else:
        attach_to_form(form, variables)

    return render(request, "admin/configuration.html",
                  {"form": form})
