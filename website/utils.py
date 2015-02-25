""" Useful utility methods. """
import re
from json import JSONEncoder, dumps
from django.db import models
from django.forms.models import model_to_dict
from functools import partial
import datetime


def custom_strftime(format, t):
    """ Custom strftime that allows date suffixes. """
    def suffix(d):
        return 'th' if 11 <= d <= 13 else \
            {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def convert_to_underscore(name):
    """ Convert CamelCase string to underscore_separated. """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class DjangoJSONEncoder(JSONEncoder):

    """ Dump JSON, using model_to_dict for django models. """

    def default(self, obj):
        """ Dump JSON, using model_to_dict for django models. """
        if isinstance(obj, models.Model):
            return model_to_dict(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)


dump_django = partial(dumps, cls=DjangoJSONEncoder)
