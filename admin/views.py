""" Admin views. """
from django.shortcuts import render, redirect
from happening.utils import admin_required
from django.conf import settings
import importlib
from django.contrib import messages
from models import PluginSetting


@admin_required
def index(request):
    """ Admin dashboard. """
    return render(request, "admin/index.html")


def format_plugin(plugin_id, plugin):
    """ Return a single formatted plugin.

    Format is (id, name, description, enabled)
    """
    enabled = False

    preference = PluginSetting.objects.filter(plugin_name=plugin_id).first()
    if preference:
        enabled = preference.enabled

    return (plugin_id, plugin.Plugin.name, plugin.Plugin.__doc__, enabled)


def save_plugins(request, plugins):
    """ Save plugin preferences to the database. """
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
    """ Plugin settings. """

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
