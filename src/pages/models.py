"""Page models."""
from django.db import models
from happening import db
from django_pgjson.fields import JsonField
from pages import utils
from happening.plugins import plugin_enabled


class Page(db.Model):

    """A static page."""

    url = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    content = JsonField(default={"blockLists": [[], []], "blocks": []})

    @property
    def filtered_block_lists(self):
        """Get the content with unusable blocks filtered out.

        This will take plugins into account.
        """
        def get_plugin_id(block):
            return utils.block_types[block["type"]].__class__.__module__[:-12]

        def filter_block_list_item(id):
            block = [b for b in self.content["blocks"] if b["id"] == id][0]
            return plugin_enabled(get_plugin_id(block))

        def map_block_lists(block_list):
            return filter(filter_block_list_item, block_list)

        return map(map_block_lists, self.content["blockLists"])
