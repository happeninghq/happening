"""Test filtering."""

from happening.tests import TestCase
from model_mommy import mommy
from django.conf import settings
from happening import filtering


class TestFiltering(TestCase):

    """Test filtering."""

    def test_simple_filter(self):
        """Test simply filter all Members."""
        # Create 5 users
        for i in range(1, 6):
            mommy.make(settings.AUTH_USER_MODEL, id=i)

        results = filtering.query("")
        self.assertEqual(len(results), 5)

    def test_filter_by_id(self):
        """Test filter by id."""
        # Create 5 users
        for i in range(1, 6):
            mommy.make(settings.AUTH_USER_MODEL, id=i)

        results = filtering.query("id:1")
        self.assertEqual(results[0].id, 1)

        results = filtering.query("id:3")
        self.assertEqual(results[0].id, 3)

    def test_filter_using_gt(self):
        """Test using django __gt filter (if this works, others will)."""
        # Create 5 users
        for i in range(1, 6):
            mommy.make(settings.AUTH_USER_MODEL, id=i)

        results = filtering.query("")
        self.assertEqual(len(results), 5)

        results = filtering.query("id__gt:1")
        self.assertEqual(len(results), 4)

    def test_filter_related(self):
        """Test getting members who have tickets for a given event."""
        # Create 5 users
        user1 = mommy.make(settings.AUTH_USER_MODEL)
        user2 = mommy.make(settings.AUTH_USER_MODEL)
        user3 = mommy.make(settings.AUTH_USER_MODEL)
        mommy.make(settings.AUTH_USER_MODEL)

        event1 = mommy.make("Event")
        event2 = mommy.make("Event")
        mommy.make("Ticket", event=event1, user=user1)
        mommy.make("Ticket", event=event1, user=user3, cancelled=True)
        mommy.make("Ticket", event=event2, user=user2)
        mommy.make("Ticket", event=event2, user=user1, cancelled=True)

        # Members who have tickets
        results = filtering.query("tickets__count__gt:0")
        self.assertEqual(len(results), 3)

        # Members who have tickets to event 1
        results = filtering.query("tickets__event__id:%s" % event1.pk)
        self.assertEqual(len(results), 2)

        # Members who have cancelled tickets for event 1
        results = filtering.query(
            "tickets__has:(event__id:%s cancelled:True)" % event1.id)
        self.assertEqual(len(results), 1)

        # Members who have tickets for event 1 and 2
        results = filtering.query("tickets__has:(event__id:%s) " % event1.id +
                                  "tickets__has:(event__id:%s)" % event2.id)
        self.assertEqual(len(results), 1)

    def test_filter_tags(self):
        """Test that we can filter members by tags."""
        user1 = mommy.make(settings.AUTH_USER_MODEL)
        mommy.make(settings.AUTH_USER_MODEL)

        results = filtering.query("tags__has:(tag:test)")
        self.assertEqual(len(results), 0)

        tag = mommy.make("Tag", tag="test")
        tag.users.add(user1)

        results = filtering.query("tags__has:(tag:test)")
        self.assertEqual(len(results), 1)

    def test_filter_individual_match(self):
        """Test we can check if a user matches a filter."""
        user1 = mommy.make(settings.AUTH_USER_MODEL)

        self.assertFalse(filtering.matches(user1, "tags__has:(tag:test)"))

        tag = mommy.make("Tag", tag="test")
        tag.users.add(user1)

        self.assertTrue(filtering.matches(user1, "tags__has:(tag:test)"))
