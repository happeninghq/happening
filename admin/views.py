"""Admin views."""
from django.shortcuts import render, redirect, get_object_or_404
from happening.utils import admin_required
from django.conf import settings
import importlib
from django.contrib import messages
from models import PluginSetting
from happening.configuration import get_configuration_variables
from happening.configuration import attach_to_form
from happening.configuration import save_variables
from forms import ConfigurationForm, ThemeForm, SocialAppForm
from happening import plugins as happening_plugins
from payments.models import PaymentHandler
from django.db import transaction
from forms import PaymentHandlerForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import re
from django.http import HttpResponseForbidden
from django.contrib.sites.models import Site
from happening.appearance import generate_css as happening_generate_css
from happening.appearance import parse_settings
from happening.storage import storage
from django import forms
from html5.forms import widgets as html5_widgets
from allauth.socialaccount.models import SocialApp


@admin_required
def index(request):
    """Admin dashboard."""
    return render(request, "admin/index.html")


def format_plugin(plugin_id, plugin):
    """Return a single formatted plugin.

    Format is (id, name, enabled)
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

    # Then clear the cache
    happening_plugins.enabled_plugins_cache = None
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
    variables = get_configuration_variables("configuration")
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


@admin_required
def payment_handlers(request):
    """List payment handlers."""
    payment_handlers = PaymentHandler.objects.all()
    return render(request, "admin/payment_handlers/index.html",
                  {"payment_handlers": payment_handlers})


@admin_required
def add_payment_handler(request):
    """Add a payment handler."""
    form = PaymentHandlerForm()
    if request.method == "POST":
        form = PaymentHandlerForm(request.POST)
        if form.is_valid():
            payment_handler = form.save()
            if PaymentHandler.objects.all().count() == 1:
                # If it's the only one it has to be active
                payment_handler.active = True
                payment_handler.save()
            messages.success(request, "Payment Handler added.")
            return redirect("payment_handlers")
    return render(request, "admin/payment_handlers/add.html", {"form": form})


@admin_required
@require_POST
def delete_payment_handler(request, pk):
    """Delete a payment handler."""
    payment_handler = get_object_or_404(PaymentHandler, pk=pk)
    if payment_handler.active:
        # We need to pass active to another
        next_active = PaymentHandler.objects.exclude(pk=pk).first()
        if next_active:
            next_active.active = True
            next_active.save()
    payment_handler.delete()
    messages.success(request, "Payment Handler deleted.")
    return redirect("payment_handlers")


@admin_required
def edit_payment_handler(request, pk):
    """Edit a payment handler."""
    payment_handler = get_object_or_404(PaymentHandler, pk=pk)
    form = PaymentHandlerForm(instance=payment_handler)
    if request.method == "POST":
        form = PaymentHandlerForm(request.POST, instance=payment_handler)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment Handler updated.")
            return redirect("payment_handlers")
    return render(request, "admin/payment_handlers/edit.html",
                  {"form": form, "payment_handler": payment_handler})


@admin_required
def make_active_payment_handler(request, pk):
    """Make a payment handler active."""
    with transaction.atomic():
        payment_handler = get_object_or_404(PaymentHandler, pk=pk)
        payment_handler.active = True
        payment_handler.save()

        PaymentHandler.objects.exclude(pk=pk).update(active=False)
    messages.success(request, "Active Payment Handler changed.")
    return redirect("payment_handlers")


@admin_required
def appearance(request):
    """Allow configuring logo and css."""
    site = Site.objects.first().happening_site

    variables = []
    with open("static/sass/settings.scss") as f:
        settings = parse_settings(f.read())

    initial_data = {"logo": site.logo}

    def setup_form(form):
        for category, items in settings.items():
            for item, value in items.items():
                form.fields[item] = forms.CharField(
                    widget=html5_widgets.ColorInput,
                    label=item.replace("-", " ").title())
                if item in site.theme_settings:
                    initial_data[item] = site.theme_settings[item]
                else:
                    initial_data[item] = value
                variables.append(item)

    form = ThemeForm(initial=initial_data)
    setup_form(form)

    if request.method == "POST":
        form = ThemeForm(request.POST)
        setup_form(form)
        if form.is_valid():
            site.theme_settings = {}
            for variable in variables:
                site.theme_settings[variable] = form.cleaned_data[variable]
            site.logo = form.cleaned_data['logo']
            site.save()

            # Regenerate CSS
            with storage.open("css/generated.css", "w+") as o:
                # This next line is S3 specific
                if hasattr(o, "_storage"):
                    o._storage.headers['Content-Type'] = 'text/css'
                d = happening_generate_css()
                o.write(d.encode('utf8'))

            return redirect("appearance")
    return render(request, "admin/appearance.html",
                  {"theme_form": form})


@admin_required
def generate_css(request):
    """Generate temporary css for use on the admin appearance panel."""
    hex_regex = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
    variables = {}
    for k, v in request.GET.items():
        variables[k] = "#" + v

        if not hex_regex.match(variables[k]):
            return HttpResponseForbidden()

    compiled = happening_generate_css(variables)
    return HttpResponse(compiled, content_type="text/css")


@admin_required
def authentication(request):
    """List social apps."""
    social_apps = SocialApp.objects.all()
    return render(request, "admin/authentication/index.html",
                  {"social_apps": social_apps})


@admin_required
def add_authentication(request):
    """Add a social app."""
    form = SocialAppForm()
    if request.method == "POST":
        form = SocialAppForm(request.POST)
        if form.is_valid():
            social_app = form.save()
            social_app.sites.add(Site.objects.first())
            messages.success(request, "Authentication provider added.")
            return redirect("authentication")
    return render(request, "admin/authentication/add.html", {"form": form})


@admin_required
@require_POST
def delete_authentication(request, pk):
    """Delete a social app."""
    social_app = get_object_or_404(SocialApp, pk=pk)
    social_app.delete()
    messages.success(request, "Authentication provider deleted.")
    return redirect("authentication")


@admin_required
def edit_authentication(request, pk):
    """Edit a social app."""
    social_app = get_object_or_404(SocialApp, pk=pk)
    form = SocialAppForm(instance=social_app)
    if request.method == "POST":
        form = SocialAppForm(request.POST, instance=social_app)
        if form.is_valid():
            form.save()
            messages.success(request, "Authentication provider updated.")
            return redirect("authentication")
    return render(request, "admin/authentication/edit.html",
                  {"form": form, "social_app": social_app})
