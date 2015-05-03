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


def staff_member_required(view_func, **kwargs):
    """Require a staff member, and log in with the correct url."""
    if 'login_url' not in kwargs:
        kwargs['login_url'] = 'account_login'
    return smr(view_func, **kwargs)


def admin_required(view_func, **kwargs):
    """Require a superuser."""
    if 'login_url' not in kwargs:
        kwargs['login_url'] = 'account_login'
    return user_passes_test(lambda u: u.is_superuser, kwargs)(view_func)


def custom_strftime(format, t):
    """Custom strftime that allows date suffixes."""
    def suffix(d):
        return 'th' if 11 <= d <= 13 else \
            {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def convert_to_underscore(name):
    """Convert CamelCase string to underscore_separated."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_to_spaces(name):
    """Convert CamelCase string to Space Separated."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)


def convert_to_camelcase(value):
    """Convert underscore_separated string to CamelCase."""
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
