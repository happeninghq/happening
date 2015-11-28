"""Event utilities."""

from json import JSONEncoder, dumps
from functools import partial
import datetime
from django.db import models


class PresetJSONEncoder(JSONEncoder):

    """Dump JSON, with specific features for event presets."""

    def default(self, obj):
        """Dump JSON, with specific features for event presets."""
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, models.fields.files.FieldFile):
            try:
                return obj.url
            except ValueError:
                return None
        return JSONEncoder.default(self, obj)


dump_preset = partial(dumps, cls=PresetJSONEncoder)
