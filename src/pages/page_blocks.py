from .utils import BlockType, register_block_type
from django import forms
from happening.forms import MarkdownField
from django.template.loader import render_to_string
from events.models import Event


@register_block_type
class TextBlockType(BlockType):
    """A block of text."""

    title = forms.CharField()
    text = MarkdownField()

    def render_content(self, request, data):
        """Render the text."""
        return data['text']


@register_block_type
class HTMLBlockType(BlockType):
    """A block of HTML."""

    title = forms.CharField()
    html = forms.CharField()

    def render_content(self, request, data):
        """Render the HTML."""
        return data['html']


@register_block_type
class FutureEventsBlockType(BlockType):
    """Show upcoming events."""

    max_events = forms.IntegerField()

    def get_future_events(self):
        """Get future events."""
        return [e for e in Event.objects.order_by('-start') if e.is_future]

    def render(self, request, data):
        """Render each event in its own block."""
        future_events = self.get_future_events()
        return render_to_string("page_blocks/future_events.html",
                                {"future_events": future_events,
                                 "future_events_sliced":
                                    future_events[:int(data.get(
                                        "max_events", 2))]},
                                request=request)

    def render_content(self, request, data):
        """Return the first event, or nothing."""
        events = self.get_future_events()
        if len(events) == 0:
            return ""
        return render_to_string("events/_event_block.html",
                                {"event": events[0]},
                                request=request)


@register_block_type
class PastEventsBlockType(BlockType):
    """Show past events."""

    max_events = forms.IntegerField()

    def get_past_events(self):
        """Get past events."""
        return [e for e in Event.objects.order_by('-start') if not e.is_future]

    def render(self, request, data):
        """Return each event in its own block."""
        past_events = self.get_past_events()

        return render_to_string("page_blocks/past_events.html",
                                {"past_events": past_events,
                                 "past_events_sliced":
                                    past_events[:int(data.get(
                                        "max_events", 2))]},
                                request=request)

    def render_content(self, request, data):
        """Return the first event, or nothing."""
        events = self.get_past_events()
        if len(events) == 0:
            return ""
        return render_to_string("events/_event_block.html",
                                {"event": events[0]},
                                request=request)


@register_block_type
class WelcomeBlockType(BlockType):
    """Welcome a user to the site."""

    title = forms.CharField()

    def render_content(self, request, data):
        """Welcome the user."""
        return render_to_string("page_blocks/welcome.html",
                                request=request)
