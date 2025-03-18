"""
Tests for our models
"""

# Standard Library
from unittest.mock import patch

# Django
from django.db import IntegrityError
from django.test import TestCase

# AA Intel Tool
from aa_intel_tool.models import Scan, ScanData


class TestScanModel(TestCase):
    """
    Test the Scan model
    """

    def test_generates_unique_hash(self):
        """
        Test that the hash is unique

        :return:
        :rtype:
        """

        hash1 = Scan.generate_scan_hash()
        hash2 = Scan.generate_scan_hash()

        self.assertNotEqual(hash1, hash2)

    def test_generates_hash_of_correct_length(self):
        """
        Test that the hash is of the correct length

        :return:
        :rtype:
        """

        scan_hash = Scan.generate_scan_hash()

        self.assertEqual(len(scan_hash), 30)

    def test_generates_hash_not_in_database(self):
        """
        Test that the generated hash is not in the database

        :return:
        :rtype:
        """

        existing_scan = Scan.objects.create(raw_data="test data")
        scan_hash = Scan.generate_scan_hash()

        self.assertNotEqual(scan_hash, existing_scan.hash)

    def test_handles_collision_by_generating_new_hash(self):
        """
        Test that the hash collision is handled by generating a new hash

        :return:
        :rtype:
        """

        with patch("aa_intel_tool.models.Scan.objects.filter") as mock_filter:
            # Simulate hash collision by returning True for the first two calls
            mock_filter.return_value.exists.side_effect = [True, True, False]

            new_hash = Scan.generate_scan_hash()

            self.assertIsNotNone(new_hash)
            self.assertEqual(len(new_hash), 30)
            self.assertNotIn(new_hash, ["collision_hash1", "collision_hash2"])

    def test_saves_with_generated_hash(self):
        """
        Test that the hash is generated on save

        :return:
        :rtype:
        """

        scan = Scan(raw_data="test data")
        scan.save()

        self.assertIsNotNone(scan.hash)
        self.assertEqual(len(scan.hash), 30)

    def test_generates_new_hash_if_empty_on_save(self):
        """
        Test that a new hash is generated if the hash is empty on save

        :return:
        :rtype:
        """

        scan = Scan(hash="", raw_data="test data")
        scan.save()

        self.assertNotEqual(scan.hash, "")
        self.assertEqual(len(scan.hash), 30)

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


class TestScanDataModel(TestCase):
    """
    Test the ScanData model
    """

    def test_creates_scan_data_with_valid_section(self):
        """
        Test that the ScanData model can be created with a valid section

        :return:
        :rtype:
        """

        scan = Scan.objects.create(raw_data="test data")
        scan_data = ScanData.objects.create(
            scan=scan,
            section=ScanData.Section.PILOTLIST,
            processed_data={"key": "value"},
        )

        self.assertEqual(scan_data.section, ScanData.Section.PILOTLIST)
        self.assertEqual(scan_data.processed_data, {"key": "value"})

    def test_defaults_to_invalid_section(self):
        """
        Test that the ScanData model defaults to INVALID section if not specified

        :return:
        :rtype:
        """

        scan = Scan.objects.create(raw_data="test data")
        scan_data = ScanData.objects.create(scan=scan, processed_data={"key": "value"})

        self.assertEqual(scan_data.section, ScanData.Section.INVALID)

    def test_allows_null_scan(self):
        """
        Test that the ScanData model allows null scan

        :return:
        :rtype:
        """

        scan_data = ScanData.objects.create(
            section=ScanData.Section.PILOTLIST, processed_data={"key": "value"}
        )

        self.assertIsNone(scan_data.scan)

    def test_enforces_unique_together_constraint(self):
        """
        Test that the ScanData model enforces unique together constraint on scan and section and raises IntegrityError

        :return:
        :rtype:
        """

        scan = Scan.objects.create(raw_data="test data")
        ScanData.objects.create(
            scan=scan,
            section=ScanData.Section.PILOTLIST,
            processed_data={"key": "value"},
        )

        with self.assertRaises(IntegrityError):
            ScanData.objects.create(
                scan=scan,
                section=ScanData.Section.PILOTLIST,
                processed_data={"key": "another value"},
            )

    def test_allows_different_sections_for_same_scan(self):
        """
        Test that the ScanData model allows different sections for the same scan

        :return:
        :rtype:
        """

        scan = Scan.objects.create(raw_data="test data")
        scan_data1 = ScanData.objects.create(
            scan=scan,
            section=ScanData.Section.PILOTLIST,
            processed_data={"key": "value"},
        )
        scan_data2 = ScanData.objects.create(
            scan=scan,
            section=ScanData.Section.CORPORATIONLIST,
            processed_data={"key": "value"},
        )

        self.assertNotEqual(scan_data1.section, scan_data2.section)
