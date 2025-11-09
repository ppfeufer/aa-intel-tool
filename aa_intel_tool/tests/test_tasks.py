"""
Unit tests for the tasks in aa_intel_tool.
"""

# Standard Library
from datetime import timedelta
from unittest.mock import patch

# Django
from django.utils.timezone import now

# AA Intel Tool
from aa_intel_tool.tasks import housekeeping
from aa_intel_tool.tests import BaseTestCase


class TestHousekeeping(BaseTestCase):
    """
    Tests for the housekeeping task
    """

    def test_removes_scans_older_than_retention_time(self):
        """
        Test that scans older than the retention time are removed.

        :return:
        :rtype:
        """

        with (
            patch("aa_intel_tool.tasks.AppSettings.INTELTOOL_SCAN_RETENTION_TIME", 7),
            patch("aa_intel_tool.tasks.Scan.objects.filter") as mock_filter,
        ):
            housekeeping()
            mock_filter.assert_called_once()
            called_kwargs = mock_filter.call_args.kwargs
            created_lte = called_kwargs.get("created__lte")
            expected = now() - timedelta(days=7)

            self.assertTrue(abs(created_lte - expected) < timedelta(seconds=1))
            mock_filter.return_value.delete.assert_called_once()

    def test_does_not_remove_scans_when_retention_time_is_zero(self):
        """
        Test that no scans are removed when retention time is set to zero.

        :return:
        :rtype:
        """

        with (
            patch("aa_intel_tool.tasks.AppSettings.INTELTOOL_SCAN_RETENTION_TIME", 0),
            patch("aa_intel_tool.tasks.Scan.objects.filter") as mock_filter,
        ):
            housekeeping()
            mock_filter.assert_not_called()
