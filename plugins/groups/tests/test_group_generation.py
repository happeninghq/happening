"""Test group generation algorithm."""

from unittest import TestCase
from plugins.groups import generate_groups


class TestGroupGeneration(TestCase):

    """Test group generation algorithm."""

    def test_sets_up_single_groups(self):
        """Test that users can be placed into single groups."""
        users = [1, 2, 3, 4, 5]
        groups = generate_groups(users, 5)
        self.assertEqual(len(groups), 5)
        self.assertIn([1], groups)
        self.assertIn([2], groups)
        self.assertIn([3], groups)
        self.assertIn([4], groups)
        self.assertIn([5], groups)

    def test_one_large_group(self):
        """Test that users can be placed into a large group."""
        users = [1, 2, 3, 4, 5]
        groups = generate_groups(users, 1)
        self.assertEqual(len(groups), 1)
        # Reversed just because of using pop()
        self.assertIn([5, 4, 3, 2, 1], groups)

    def test_evenly_sized_groups(self):
        """Test that users can be placed into evenly sized groups."""
        users = [1, 2, 3, 4]
        groups = generate_groups(users, 2)
        self.assertEqual(len(groups), 2)
        self.assertIn([4, 2], groups)
        self.assertIn([3, 1], groups)

    def test_unevenly_sized_groups(self):
        """Test that users can be placed into unevenly sized groups."""
        users = [1, 2, 3, 4, 5]
        groups = generate_groups(users, 2)
        self.assertEqual(len(groups), 2)
        self.assertIn([5, 3, 1], groups)
        self.assertIn([4, 2], groups)

        users = [1, 2, 3, 4, 5, 6, 7, 8]
        groups = generate_groups(users, 3)
        self.assertEqual(len(groups), 3)
        self.assertIn([8, 5, 2], groups)
        self.assertIn([7, 4, 1], groups)
        self.assertIn([6, 3], groups)

    def test_evenly_sized_groups_with_existing(self):
        """Test generating evenly sized groups with existing groups."""
        users = [2, 4]
        existing_groups = {0: [1], 1: [3]}
        groups = generate_groups(users, 2, existing_groups)
        self.assertEqual(len(groups), 2)
        self.assertIn([1, 4], groups)
        self.assertIn([3, 2], groups)

    def test_unevenly_sized_groups_with_existing(self):
        """Test generating uneven groups with existing groups."""
        users = [2, 4]
        existing_groups = {0: [1], 1: [3, 5]}
        groups = generate_groups(users, 2, existing_groups)
        self.assertEqual(len(groups), 2)
        self.assertIn([1, 4, 2], groups)
        self.assertIn([3, 5], groups)

        users = [2, 4]
        existing_groups = {0: [1], 1: [3, 5, 6]}
        groups = generate_groups(users, 2, existing_groups)
        self.assertEqual(len(groups), 2)
        self.assertIn([1, 4, 2], groups)
        self.assertIn([3, 5, 6], groups)

    def test_unevenly_sized_groups_with_late_existing(self):
        """Test generating uneven groups with existing later groups."""
        users = [1, 2, 4]
        existing_groups = {2: [3, 5]}
        groups = generate_groups(users, 3, existing_groups)
        self.assertEqual(len(groups), 3)
        self.assertIn([4, 1], groups)
        self.assertIn([2], groups)
        self.assertIn([3, 5], groups)
