from django import forms
from django.utils.html import mark_safe

block_types = {}


def register_block_type(b):
    """Register a block type for use on pages."""
    name = b.__name__.replace("BlockType", "").lower()
    block_types[name] = b()
    return b


def get_fields(c):
    """Get fields in a block type."""
    return [{"name": k, "type": v.widget.__class__.__name__} for k, v in
            c.__class__.__dict__.items() if
            issubclass(v.__class__, forms.Field)]


class BlockType(object):
    """A block type that can be rendered on a page."""

    def render_content(self, request, data):
        """Render just the content of the block (no header)."""
        return ""

    def render(self, request, data):
        """Render the entire block."""
        return """
            <div class="block-list__item block">
                <header class="block__header">
                    <h2 class="block__header-text block__header-text--small">
                        %s
                    </h2>
                </header>

                %s
            </div>
        """ % (data.get("title", ""), self.render_content(request, data))


def render_block(block, request):
    """Render the entire block."""
    return mark_safe(block_types[block["type"].lower()].render(request, block))


def render_block_content(block, request):
    """Render just the content of the block (no header)."""
    return mark_safe(block_types[block["type"].lower()].render_content(request,
                     block))


def get_block_types():
    """Get available block types."""
    return [{"type": name, "fields": get_fields(c)} for name, c in
            block_types.items()]
