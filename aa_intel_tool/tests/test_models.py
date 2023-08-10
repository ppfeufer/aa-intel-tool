"""
Tests for our models
"""

# Django
from django.test import TestCase

# AA Intel Tool
from aa_intel_tool.models import Scan


class TestScan(TestCase):
    """
    Tests for the board model
    """

    def test_model_string_names(self):
        """
        Test model string name

        :return:
        :rtype:
        """

        scan = Scan(
            raw_data="Foobar",
        )
        scan.save()
        expected_hash = scan.hash
        self.assertEqual(first=str(scan), second=expected_hash)

        scan.raw_data = "BarFoo"
        scan.save()
        self.assertEqual(first=str(scan), second=expected_hash)

        scan.hash = ""
        scan.save()
        self.assertNotEqual(first=str(scan), second="")
        self.assertNotEqual(first=str(scan), second=expected_hash)

        scan.save()
