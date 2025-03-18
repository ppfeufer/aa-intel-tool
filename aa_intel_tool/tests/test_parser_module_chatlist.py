"""
Test cases for the chatlist parser module.
"""

# Standard Library
from unittest import TestCase
from unittest.mock import MagicMock, patch

# AA Intel Tool
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.models import Scan
from aa_intel_tool.parser.module.chatlist import parse


class TestParse(TestCase):
    """
    Test cases for the parse function in the chatlist module.
    """

    @patch(
        "aa_intel_tool.parser.module.chatlist.AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN",
        True,
    )
    @patch("aa_intel_tool.parser.module.chatlist._get_character_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_chatscan_data")
    @patch("aa_intel_tool.parser.module.chatlist.safe_scan_to_db")
    def test_parses_valid_scan_data(
        self, mock_safe_scan_to_db, mock_parse_chatscan_data, mock_get_character_info
    ):
        """
        Test should parse valid scan data and return a Scan object.

        :param mock_safe_scan_to_db:
        :type mock_safe_scan_to_db:
        :param mock_parse_chatscan_data:
        :type mock_parse_chatscan_data:
        :param mock_get_character_info:
        :type mock_get_character_info:
        :return:
        :rtype:
        """

        mock_get_character_info.return_value = MagicMock()
        mock_parse_chatscan_data.return_value = {
            "pilots": [],
            "corporations": [],
            "alliances": [],
        }
        mock_safe_scan_to_db.return_value = Scan()

        scan_data = ["Character1", "Character2"]
        result = parse(scan_data)

        self.assertIsInstance(result, Scan)

    @patch(
        "aa_intel_tool.parser.module.chatlist.AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN",
        True,
    )
    @patch("aa_intel_tool.parser.module.chatlist._get_character_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_chatscan_data")
    def test_returns_parsed_data_when_safe_to_db_is_false(
        self, mock_parse_chatscan_data, mock_get_character_info
    ):
        """
        Test should parse valid scan data and return a dictionary when safe_to_db is False.

        :param mock_parse_chatscan_data:
        :type mock_parse_chatscan_data:
        :param mock_get_character_info:
        :type mock_get_character_info:
        :return:
        :rtype:
        """

        mock_get_character_info.return_value = MagicMock()
        mock_parse_chatscan_data.return_value = {
            "pilots": [],
            "corporations": [],
            "alliances": [],
        }

        scan_data = ["Character1", "Character2"]
        result = parse(scan_data, safe_to_db=False)

        self.assertIsInstance(result, dict)

    @patch(
        "aa_intel_tool.parser.module.chatlist.AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN",
        False,
    )
    def test_raises_error_when_module_disabled(self):
        """
        Test should raise a ParserError when the module is disabled.

        :return:
        :rtype:
        """

        with self.assertRaises(ParserError):
            parse([])

    @patch(
        "aa_intel_tool.parser.module.chatlist.AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN",
        True,
    )
    @patch(
        "aa_intel_tool.parser.module.chatlist.AppSettings.INTELTOOL_CHATSCAN_MAX_PILOTS",
        1,
    )
    def test_raises_error_when_pilot_limit_exceeded(self):
        """
        Test should raise a ParserError when the pilot limit is exceeded.

        :return:
        :rtype:
        """

        scan_data = ["Character1", "Character2"]

        with self.assertRaises(ParserError):
            parse(scan_data)

    @patch(
        "aa_intel_tool.parser.module.chatlist.AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN",
        True,
    )
    @patch("aa_intel_tool.parser.module.chatlist._get_character_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_chatscan_data")
    def test_handles_empty_scan_data(
        self, mock_parse_chatscan_data, mock_get_character_info
    ):
        """
        Test should handle empty scan data gracefully.

        :param mock_parse_chatscan_data:
        :type mock_parse_chatscan_data:
        :param mock_get_character_info:
        :type mock_get_character_info:
        :return:
        :rtype:
        """

        mock_get_character_info.return_value = MagicMock()
        mock_parse_chatscan_data.return_value = {
            "pilots": [],
            "corporations": [],
            "alliances": [],
        }

        scan_data = []
        result = parse(scan_data)

        self.assertIsInstance(result, Scan)
