"""Test ticket purchasing widget."""
from happening.tests import TestCase
# from model_mommy import mommy
# from datetime import datetime, timedelta
# import pytz
# from django.conf import settings


class TestTicketWidget(TestCase):

    """Test ticket purchasing widget."""

    def test_remaining_tickets(self):
        """Test that remaining_tickets works."""
        pass

    def test_end_date(self):
        """Test that the end date is shown correctly."""
        pass

    def test_past_event(self):
        """Test that we can't buy tickets past the deadline."""
        pass

    def test_quantity(self):
        """Test that the quantity box doesn't allow > remainging tickets."""
    pass

    def test_sold_out(self):
        """Test that we can't buy tickets once they are sold out."""
        pass

    def test_lists_attending_members(self):
        """Test that the widget shows a list of attending members."""
        pass
