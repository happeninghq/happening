"""Events iCal feeds."""
from django_ical.views import ICalFeed
from models import Event
from event_configuration import Description


class AllEventsFeed(ICalFeed):

    """Feed of all events."""

    product_id = '-//happening.com//Example//EN'
    timezone = 'UTC'
    file_name = "events.ics"

    def items(self):
        """Get items in field."""
        return Event.objects.all().order_by('-start')

    def item_title(self, item):
        """Get the item title."""
        return item.title

    def item_description(self, item):
        """Pull the item description from configuration."""
        # We use raw as markdown will look better than html here
        return Description(item).get()

    def item_start_datetime(self, item):
        """Get the item start time."""
        return item.start
