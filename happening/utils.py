"""Useful utility methods."""
import re
from json import JSONEncoder, dumps
from django.db import models
from django.forms.models import model_to_dict
from functools import partial
import datetime
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required as smr
from django.contrib.auth.decorators import user_passes_test
from math import log
from django.template.loader import render_to_string
from django.template import RequestContext
from cStringIO import StringIO
import sys


def render_block(request, template, kwargs):
    """Render a block template to string."""
    return render_to_string(
        template,
        kwargs,
        context_instance=RequestContext(request))


def staff_member_required(view_func, **kwargs):
    """Require a staff member, and log in with the correct url."""
    if 'login_url' not in kwargs:
        kwargs['login_url'] = 'account_login'
    return smr(view_func, **kwargs)


def admin_required(view_func, **kwargs):
    """Require a superuser."""
    if 'login_url' not in kwargs:
        kwargs['login_url'] = 'account_login'
    return user_passes_test(lambda u: u.is_superuser, **kwargs)(view_func)


def custom_strftime(format, t):
    """Custom strftime that allows date suffixes."""
    def suffix(d):
        return 'th' if 11 <= d <= 13 else \
            {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def convert_to_underscore(name):
    """Convert CamelCase string to underscore_separated."""
    name = name.replace(" ", "")
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_to_spaces(name):
    """Convert CamelCase string to Space Separated."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)


def convert_to_camelcase(value):
    """Convert underscore_separated string to CamelCase."""
    value = value.replace(" ", "")
    return ''.join(word[0].upper() + word[1:] for word in value.split('_'))


class DjangoJSONEncoder(JSONEncoder):
    """Dump JSON, using model_to_dict for django models."""

    def default(self, obj):
        """Dump JSON, using model_to_dict for django models."""
        if isinstance(obj, models.Model):
            return model_to_dict(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, models.fields.files.FieldFile):
            try:
                return obj.url
            except ValueError:
                return None
        return JSONEncoder.default(self, obj)


dump_django = partial(dumps, cls=DjangoJSONEncoder)


def plugin_enabled_decorator(plugin):
    """Decorator which checks if a plugin is enabled.

    If the plugin is not enabled. The user will be redirected to the index.
    """
    def decorator(f):
        def inner(*args, **kwargs):
            from happening.plugins import plugin_enabled
            if not plugin_enabled(plugin):
                return redirect("index")
            return f(*args, **kwargs)
        return inner
    return decorator


def get_all_subclasses(cls):
    """Recursively get all subclasses of a given class."""
    subclasses = cls.__subclasses__()
    for s in subclasses:
        yield s
        for ss in get_all_subclasses(s):
            yield ss


def format_bytes(num, suffix='B'):
    """Format bytes as human readable."""
    unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'],
                    [0, 0, 1, 2, 2, 2])
    if num > 1:
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'


class capturing(list):
    """Capture stdout to variable."""

    def __enter__(self):
        """Capture stdout to variable."""
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        """Capture stdout to variable."""
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout
