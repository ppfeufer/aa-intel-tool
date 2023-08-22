"""
Test the app settings in local.py
"""

# Standard Library
from unittest import mock

# Django
from django.test import TestCase

# AA Intel Tool
from aa_intel_tool.app_settings import AppSettings

SETTINGS_PATH = "aa_intel_tool.app_settings"


class TestAppSettings(TestCase):
    """
    Tests for App Settings
    """

    def test_scan_retention_time_default(self):
        """
        Test for the default INTELTOOL_SCAN_RETENTION_TIME

        :return:
        :rtype:
        """

        retention_time = AppSettings.INTELTOOL_SCAN_RETENTION_TIME
        expected_retention_time = 30

        self.assertEqual(first=retention_time, second=expected_retention_time)

    @mock.patch(SETTINGS_PATH + ".AppSettings.INTELTOOL_SCAN_RETENTION_TIME", 75)
    def test_scan_retention_time_custom(self):
        """
        Test for a custom INTELTOOL_SCAN_RETENTION_TIME

        :return:
        :rtype:
        """

        retention_time = AppSettings.INTELTOOL_SCAN_RETENTION_TIME
        expected_retention_time = 75

        self.assertEqual(first=retention_time, second=expected_retention_time)

    def test_chatscan_max_pilots_default(self):
        """
        Test for the default INTELTOOL_CHATSCAN_MAX_PILOTS

        :return:
        :rtype:
        """

        max_pilots = AppSettings.INTELTOOL_CHATSCAN_MAX_PILOTS
        expected_max_pilots = 500

        self.assertEqual(first=max_pilots, second=expected_max_pilots)

    @mock.patch(SETTINGS_PATH + ".AppSettings.INTELTOOL_CHATSCAN_MAX_PILOTS", 1000)
    def test_chatscan_max_pilots_custom(self):
        """
        Test for a custom INTELTOOL_CHATSCAN_MAX_PILOTS

        :return:
        :rtype:
        """

        max_pilots = AppSettings.INTELTOOL_CHATSCAN_MAX_PILOTS
        expected_max_pilots = 1000

        self.assertEqual(first=max_pilots, second=expected_max_pilots)

    def test_dscan_grid_size(self):
        """
        Test for the default INTELTOOL_DSCAN_GRID_SIZE

        :return:
        :rtype:
        """

        grid_size = AppSettings.INTELTOOL_DSCAN_GRID_SIZE
        expected_grid_size = 10000

        self.assertEqual(first=grid_size, second=expected_grid_size)

    @mock.patch(SETTINGS_PATH + ".AppSettings.INTELTOOL_DSCAN_GRID_SIZE", 1000)
    def test_dscan_grid_size_custom(self):
        """
        Test for a custom INTELTOOL_DSCAN_GRID_SIZE

        :return:
        :rtype:
        """

        grid_size = AppSettings.INTELTOOL_DSCAN_GRID_SIZE
        expected_grid_size = 1000

        self.assertEqual(first=grid_size, second=expected_grid_size)
