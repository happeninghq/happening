from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.template import Library
import json

register = Library()


def jsonify(object):
    """Convert an object into JSON."""
    if isinstance(object, QuerySet):
        val = serialize('json', object)
    val = json.dumps(object)

    return val


register.filter('jsonify', jsonify)
jsonify.is_safe = True
