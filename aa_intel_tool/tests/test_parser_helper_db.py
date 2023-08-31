"""
Tests for the parsers' DB helper => aa_intel_tool/parser/helper/db.py
"""

# Django
from django.test import TestCase

# AA Intel Tool
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.helper.db import safe_scan_to_db


class TestParserHelperDb(TestCase):
    """
    The tests
    """

    def test_safe_scan_to_db_without_associated_data(self):
        """
        Test that the scan is successfully saved to the DB

        :return:
        :rtype:
        """

        new_scan = safe_scan_to_db(scan_type=Scan.Type.DSCAN, parsed_data={})

        from_db = Scan.objects.get(pk=new_scan.hash, scan_type__exact=Scan.Type.DSCAN)

        self.assertEqual(first=new_scan.hash, second=from_db.hash)

    def test_safe_scan_to_db_with_associated_data(self):
        """
        Test that the scan is successfully saved to the DB

        :return:
        :rtype:
        """

        parsed_data = {
            "foobar": {
                "section": ScanData.Section.PILOTLIST,
                "data": {"name": "William Riker"},
            }
        }

        new_scan = safe_scan_to_db(scan_type=Scan.Type.DSCAN, parsed_data=parsed_data)

        scan_from_db = Scan.objects.get(
            pk=new_scan.hash, scan_type__exact=Scan.Type.DSCAN
        )
        scan_data_from_db = ScanData.objects.get(
            scan_id__exact=scan_from_db.hash,
            section__exact=ScanData.Section.PILOTLIST,
        )

        self.assertEqual(first=new_scan.hash, second=scan_from_db.hash)
        self.assertEqual(
            first=scan_data_from_db.processed_data, second=parsed_data["foobar"]["data"]
        )
