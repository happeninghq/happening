"""Test appearance."""

from unittest import TestCase
from happening import appearance


class TestAppearance(TestCase):

    """Test appearance."""

    def test_parse_categories(self):
        """Test parsing categories."""
        config = """

        /**
         * Basic
         */


        /**
         * Menu
         */
        """
        categories = appearance.parse_settings(config)
        self.assertTrue("Basic" in categories)
        self.assertTrue("Menu" in categories)

    def test_parse_full_configuration(self):
        """Test parsing full configuration."""
        config = """

        /**
         * Basic
         */

         $VAR1: #FFA;
         $VAR2: #FFB;

        /**
         * Menu
         */

         $VAR3: #FFC;
         $VAR4: #FFD;
        """
        categories = appearance.parse_settings(config)
        self.assertEqual(categories["Basic"]["VAR1"], "#FFA")
        self.assertEqual(categories["Basic"]["VAR2"], "#FFB")
        self.assertEqual(categories["Menu"]["VAR3"], "#FFC")
        self.assertEqual(categories["Menu"]["VAR4"], "#FFD")
