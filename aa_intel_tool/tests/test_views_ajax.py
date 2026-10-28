"""
Tests for the AJAX views in aa_intel_tool.views.ajax.
"""

# Standard Library
from http import HTTPStatus
from unittest.mock import Mock, patch

# Django
from django.test import RequestFactory
from django.urls import reverse

# AA Intel Tool
from aa_intel_tool.models import ScanData
from aa_intel_tool.tests import BaseTestCase
from aa_intel_tool.views.ajax import get_scan_data


class TestGetScanData(BaseTestCase):
    """
    Tests for the get_scan_data AJAX view
    """

    def test_returns_processed_data_for_valid_scan_hash_and_section(self):
        """
        Testing return of processed data for valid scan hash and section

        :return:
        :rtype:
        """

        scan_uuid = "00000000-0000-0000-0000-000000000001"
        rf = RequestFactory()
        request = rf.get(
            reverse(
                "aa_intel_tool:ajax_get_scan_data",
                kwargs={"scan": scan_uuid, "scan_section": "valid-section"},
            )
        )

        with patch("aa_intel_tool.views.ajax.ScanData.objects.filter") as mock_filter:
            mock_scan_data = Mock()
            mock_scan_data.processed_data = {"key": "value"}
            mock_filter.return_value.get.return_value = mock_scan_data

            response = get_scan_data(request, scan_uuid, "valid-section")

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertJSONEqual(response.content, {"key": "value"})

    def test_returns_empty_dict_when_scan_data_does_not_exist(self):
        """
        Testing return of empty dict when scan data does not exist

        :return:
        :rtype:
        """

        scan_uuid = "00000000-0000-0000-0000-000000000002"
        rf = RequestFactory()
        request = rf.get(
            reverse(
                "aa_intel_tool:ajax_get_scan_data",
                kwargs={"scan": scan_uuid, "scan_section": "invalid-section"},
            )
        )

        with patch("aa_intel_tool.views.ajax.ScanData.objects.filter") as mock_filter:
            mock_filter.return_value.get.side_effect = ScanData.DoesNotExist

            response = get_scan_data(request, scan_uuid, "invalid-section")

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertJSONEqual(response.content, {})
