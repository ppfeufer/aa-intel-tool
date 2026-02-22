"""
Test the app settings in local.py
"""

# Standard Library
import importlib
from unittest import mock

# Django
from django.conf import settings
from django.test import override_settings

# AA Intel Tool
from aa_intel_tool import app_settings
from aa_intel_tool.app_settings import AppSettings, _clean_setting, debug_enabled
from aa_intel_tool.tests import BaseTestCase

SETTINGS_PATH = "aa_intel_tool.app_settings"


class TestHelperCleanSetting(BaseTestCase):
    """
    Tests for the _clean_setting helper function
    """

    def test_returns_default_value_when_setting_is_absent(self):
        """
        Test returns default value when setting is absent

        :return:
        :rtype:
        """

        if hasattr(settings, "TEST_SETTING"):
            delattr(settings, "TEST_SETTING")

        result = _clean_setting("TEST_SETTING", default_value=123, required_type=int)

        self.assertEqual(result, 123)

    def test_returns_setting_value_when_valid_and_defined(self):
        """
        Test returns setting value when valid and defined

        :return:
        :rtype:
        """

        with self.settings(TEST_SETTING=456):
            result = _clean_setting(
                "TEST_SETTING", default_value=123, required_type=int
            )

            self.assertEqual(result, 456)

    def test_raises_value_error_when_default_is_below_minimum(self):
        """
        Test raises ValueError when default is below minimum

        :return:
        :rtype:
        """

        with self.assertRaises(ValueError):
            _clean_setting(
                "TEST_SETTING", default_value=5, min_value=10, required_type=int
            )

    def test_raises_value_error_when_default_exceeds_maximum(self):
        """
        Test raises ValueError when default exceeds maximum

        :return:
        :rtype:
        """

        with self.assertRaises(ValueError):
            _clean_setting(
                "TEST_SETTING", default_value=15, max_value=10, required_type=int
            )

    def test_uses_minimum_value_when_setting_is_below_minimum(self):
        """
        Test uses minimum value when setting is below minimum

        :return:
        :rtype:
        """

        with self.settings(TEST_SETTING=5):
            result = _clean_setting(
                "TEST_SETTING", default_value=123, min_value=10, required_type=int
            )

            self.assertEqual(result, 10)

    def test_uses_maximum_value_when_setting_exceeds_maximum(self):
        """
        Test uses maximum value when setting exceeds maximum

        :return:
        :rtype:
        """

        with self.settings(TEST_SETTING=15):
            result = _clean_setting(
                "TEST_SETTING", default_value=3, max_value=10, required_type=int
            )

            self.assertEqual(result, 10)

    def test_raises_type_error_when_required_type_is_invalid(self):
        """
        Test raises TypeError when required_type is invalid

        :return:
        :rtype:
        """

        with self.assertRaises(TypeError):
            _clean_setting(
                "TEST_SETTING", default_value=123, required_type="not_a_type"
            )

    def test_raises_value_error_when_required_type_is_missing_for_none_default(self):
        """
        Test raises ValueError when required_type is missing for None default

        :return:
        :rtype:
        """

        with self.assertRaises(ValueError):
            _clean_setting("TEST_SETTING", default_value=None)

    def test_uses_default_value_when_setting_is_not_in_choices(self):
        """
        Test uses default value when setting is not in choices

        :return:
        :rtype:
        """

        with self.settings(TEST_SETTING=999):
            result = _clean_setting(
                "TEST_SETTING", default_value=123, required_type=int, choices=[1, 2, 3]
            )

            self.assertEqual(result, 123)

    def test_uses_setting_value_when_in_choices(self):
        """
        Test uses setting value when in choices

        :return:
        :rtype:
        """

        with self.settings(TEST_SETTING=2):
            result = _clean_setting(
                "TEST_SETTING", default_value=123, required_type=int, choices=[1, 2, 3]
            )

            self.assertEqual(result, 2)

    def test_uses_type_of_default_value_when_required_type_is_not_provided(self):
        """
        Test uses type of default value when required_type is not provided

        :return:
        :rtype:
        """

        result = _clean_setting("TEST_SETTING", default_value=123)

        self.assertEqual(result, 123)

    def test_raises_type_error_when_default_value_is_none_and_required_type_is_not_provided(
        self,
    ):
        """
        Test raises TypeError when default_value is None and required_type is not provided

        :return:
        :rtype:
        """

        with self.assertRaises(ValueError):
            _clean_setting("TEST_SETTING", default_value=None)

    def test_does_not_raise_error_when_required_type_is_subclass_of_int(self):
        """
        Test does not raise error when required_type is subclass of int

        :return:
        :rtype:
        """

        result = _clean_setting("TEST_SETTING", default_value=123, required_type=int)

        self.assertEqual(result, 123)

    def test_skips_check_when_default_value_is_none_and_required_type_is_subclass_of_int(
        self,
    ):
        """
        Test skips check when default_value is None and required_type is subclass of int

        :return:
        :rtype:
        """

        result = _clean_setting("TEST_SETTING", default_value=None, required_type=int)

        self.assertIsNone(result)


class TestAppSettings(BaseTestCase):
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

    # @mock.patch(SETTINGS_PATH + ".AppSettings.INTELTOOL_SCAN_RETENTION_TIME", 75)
    def test_scan_retention_time_custom(self):
        """
        Test for a custom INTELTOOL_SCAN_RETENTION_TIME

        :return:
        :rtype:
        """

        reloaded_module = importlib.reload(app_settings)

        with mock.patch.object(
            reloaded_module.AppSettings, "INTELTOOL_SCAN_RETENTION_TIME", 75
        ):
            retention_time = reloaded_module.AppSettings.INTELTOOL_SCAN_RETENTION_TIME
            expected_retention_time = 75

            self.assertEqual(first=retention_time, second=expected_retention_time)

    @override_settings()
    def test_chatscan_max_pilots_default(self):
        """
        Test for the default INTELTOOL_CHATSCAN_MAX_PILOTS

        :return:
        :rtype:
        """

        if hasattr(settings, "INTELTOOL_CHATSCAN_MAX_PILOTS"):
            delattr(settings, "INTELTOOL_CHATSCAN_MAX_PILOTS")

        reloaded_module = importlib.reload(app_settings)
        max_pilots = reloaded_module.AppSettings.INTELTOOL_CHATSCAN_MAX_PILOTS
        expected_max_pilots = 500

        print("max_pilots:", max_pilots)

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

    # @mock.patch(SETTINGS_PATH + ".AppSettings.INTELTOOL_DSCAN_GRID_SIZE", 1000)
    def test_dscan_grid_size_custom(self):
        """
        Test for a custom INTELTOOL_DSCAN_GRID_SIZE

        :return:
        :rtype:
        """

        reloaded_module = importlib.reload(app_settings)

        with mock.patch.object(
            reloaded_module.AppSettings, "INTELTOOL_DSCAN_GRID_SIZE", 1000
        ):
            grid_size = reloaded_module.AppSettings.INTELTOOL_DSCAN_GRID_SIZE
            expected_grid_size = 1000

            self.assertEqual(first=grid_size, second=expected_grid_size)

    @override_settings(DEBUG=True)
    def test_debug_enabled_with_debug_true(self) -> None:
        """
        Test debug_enabled with DEBUG = True

        :return:
        :rtype:
        """

        self.assertTrue(debug_enabled())

    @override_settings(DEBUG=False)
    def test_debug_enabled_with_debug_false(self) -> None:
        """
        Test debug_enabled with DEBUG = False

        :return:
        :rtype:
        """

        self.assertFalse(debug_enabled())
