"""
Tests for our models
"""

# Django
from django.db import IntegrityError

# AA Intel Tool
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.tests import BaseTestCase


class TestScanModel(BaseTestCase):
    """
    Test the Scan model
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
        expected_hash = str(scan.pk)

        self.assertEqual(first=str(scan), second=expected_hash)

        scan.raw_data = "BarFoo"
        scan.save()

        self.assertEqual(first=str(scan), second=expected_hash)

        self.assertNotEqual(first=str(scan), second="")
        self.assertEqual(first=str(scan), second=expected_hash)


class TestScanDataModel(BaseTestCase):
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
