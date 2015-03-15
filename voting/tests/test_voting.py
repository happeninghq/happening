"""Test voting algorithm."""

from unittest import TestCase
from voting import AVVote


class TestVoting(TestCase):

    """Test voting algorithm."""

    def setUp(self):
        """Create AVVote."""
        self.avvote = AVVote()

    def test_basic_vote(self):
        """Test all vote for one candidate."""
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["A", "B"])
        self.assertEquals("A", self.avvote.winner)

    def test_second_choice(self):
        """Test second round."""
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["B", "A"])
        self.avvote.add_preference(["B", "A"])
        self.avvote.add_preference(["C"])
        self.avvote.add_preference(["C"])
        self.avvote.add_preference(["C"])
        self.avvote.add_preference(["C"])
        self.assertEquals("A", self.avvote.winner)

    def test_empty_voting(self):
        """Test voting with an empty preference."""
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["B", "A"])
        self.avvote.add_preference([])
        self.assertEquals("A", self.avvote.winner)

    def test_ignore_choice(self):
        """Test banning a choice from the results."""
        self.avvote = AVVote(ignore=["A"])
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["A", "B"])
        self.avvote.add_preference(["B", "A"])
        self.avvote.add_preference(["B", "A"])
        self.avvote.add_preference(["C"])
        self.avvote.add_preference(["C"])
        self.avvote.add_preference(["C"])
        self.avvote.add_preference(["C"])
        self.assertEquals("B", self.avvote.winner)
