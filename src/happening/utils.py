"""Useful utility methods."""
import re
from json import JSONEncoder, dumps
from django.db import models
from django.forms.models import model_to_dict
from functools import partial
import datetime
from django.shortcuts import redirect
from math import log
from io import StringIO
import sys
from django.template.loader import get_template
from django.contrib.sites.models import Site
from django.apps import apps
from django.conf import settings
import inspect
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from members.groups import ADMIN_GROUP
get_model = apps.get_model


def render_block(request, template, kwargs):
    """Render a block template to string."""
    return get_template(template).render(kwargs, request)


def admin_required(view_func):
    """Require a superuser. This should not be used.

        This should be replaced with require_permission.
    """
    def admin_required_inner(request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect(reverse("account_login") + "?next=%s" % request.path)
        if request.user.groups.filter(name=ADMIN_GROUP.name).count() == 0:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return admin_required_inner


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
    unit_list = list(zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'],
                     [0, 0, 1, 2, 2, 2]))
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


def externalise_urls(text):
    """Convert all URLs in a piece of text from internal to external."""
    p = re.sub('\]\((?P<pk>.+?)\)',
               lambda m: "](%s)" % externalise_url(m.group(1)), text)
    # Ideally we'd do everything as markdown - but until that is changed
    # we need to parse <a> tags too
    return re.sub('<a(?P<pk1>.*?)href="(?P<pk>.+?)"(?P<pk2>.*?)>',
                  lambda m: "<a%shref=\"%s\"%s>" % (m.group(1),
                                                    externalise_url(
                                                        m.group(2)),
                                                    m.group(3)), p)


def externalise_url(url):
    """Convert a single URL from internal to external."""
    if ":" in url:
        # Already absolute
        return url

    # We only ever use the first site
    site = Site.objects.get(pk=1)

    prefix = "https://"
    if settings.DISABLE_SSL:
        prefix = "http://"

    if not url.startswith("/"):
        url = "/" + url

    return prefix + site.domain + url


def human_delta(tdelta):
    """Take a timedelta object and formats it for humans.

    From https://gist.github.com/dhrrgn/7255361

    Usage:
    # 149 day(s) 8 hr(s) 36 min 19 sec
    print human_delta(datetime(2014, 3, 30) - datetime.now())
    Example Results:
    23 sec
    12 min 45 sec
    1 hr(s) 11 min 2 sec
    3 day(s) 13 hr(s) 56 min 34 sec
    :param tdelta: The timedelta object.
    :return: The human formatted timedelta
    """
    d = dict(days=tdelta.days)
    d['hrs'], rem = divmod(tdelta.seconds, 3600)
    d['min'], d['sec'] = divmod(rem, 60)
    if d['min'] is 0:
        fmt = '{sec} sec'
    elif d['hrs'] is 0:
        fmt = '{min} min {sec} sec'
    elif d['days'] is 0:
        fmt = '{hrs} hr(s) {min} min {sec} sec'
    else:
        fmt = '{days} day(s) {hrs} hr(s) {min} min {sec} sec'
    return fmt.format(**d)


def get_request():
    """Walk up the stack, return the nearest first argument named "request"."""
    # From http://nedbatchelder.com/blog/201008/global_django_requests.html
    # This is ugly! very temporary...
    frame = None
    try:
        for f in inspect.stack()[1:]:
            frame = f[0]
            code = frame.f_code
            if code.co_varnames and code.co_varnames[0] == "request":
                return frame.f_locals['request']
    finally:
        del frame
