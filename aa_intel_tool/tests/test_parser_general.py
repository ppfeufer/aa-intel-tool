"""
Testing the parsers
"""

# Standard Library
from unittest.mock import MagicMock, patch

# AA Intel Tool
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.parser.general import check_intel_type, parse_intel
from aa_intel_tool.tests import BaseTestCase
from aa_intel_tool.tests.utils import (
    load_chatscan_faulty_txt,
    load_chatscan_txt,
    load_dscan_txt,
    load_fleetcomp_txt,
)


class TestCheckIntelType(BaseTestCase):
    """
    Test the check_intel_type function
    """

    def test_check_intel_type_dscan(self):
        """
        Test should return 'dscan' as the expected intel type

        :return:
        :rtype:
        """

        form_data = load_dscan_txt()
        scan_data = str(form_data).splitlines()

        intel_type = check_intel_type(scan_data=scan_data)
        expected_intel_type = "dscan"

        self.assertEqual(first=intel_type, second=expected_intel_type)

    def test_check_intel_type_chatlist(self):
        """
        Test should return 'chatlist' as the expected intel type

        :return:
        :rtype:
        """

        form_data = load_chatscan_txt()
        scan_data = str(form_data).splitlines()

        intel_type = check_intel_type(scan_data=scan_data)
        expected_intel_type = "chatlist"

        self.assertEqual(first=intel_type, second=expected_intel_type)

    def test_check_intel_type_fleetcomp(self):
        """
        Test should return 'fleetcomp' as the expected intel type

        :return:
        :rtype:
        """

        form_data = load_fleetcomp_txt()
        scan_data = str(form_data).splitlines()

        intel_type = check_intel_type(scan_data=scan_data)
        expected_intel_type = "fleetcomp"

        self.assertEqual(first=intel_type, second=expected_intel_type)

    def test_check_intel_type_malformed_data(self):
        """
        Test should throw a ParserError as the expected intel type
        This happens when invalid data has been posted

        :return:
        :rtype:
        """

        form_data = load_chatscan_faulty_txt()
        scan_data = str(form_data).splitlines()

        expected_exception = ParserError
        expected_message = "A parser error occurred » No suitable parser found. Input is not a supported intel type or malformed …"

        with self.assertRaises(expected_exception=expected_exception):
            check_intel_type(scan_data=scan_data)

        with self.assertRaisesMessage(
            expected_exception=expected_exception, expected_message=expected_message
        ):
            check_intel_type(scan_data=scan_data)

    def test_parse_intel_with_invalid_form_data(self):
        """
        Test should return a ParserError as parsed intel data for invalid form data

        :return:
        :rtype:
        """

        form_data = load_chatscan_faulty_txt()

        expected_exception = ParserError
        expected_message = "A parser error occurred » No suitable parser found. Input is not a supported intel type or malformed …"

        with self.assertRaises(ParserError):
            parse_intel(form_data=form_data)

        with self.assertRaisesMessage(
            expected_exception=expected_exception, expected_message=expected_message
        ):
            parse_intel(form_data=form_data)

    def test_parse_intel_empty_form_data(self):
        """
        Test should throw a ParserError as parsed intel data for empty form data

        :return:
        :rtype:
        """

        form_data = ""

        expected_exception = ParserError
        expected_message = "A parser error occurred » No data to parse …"

        with self.assertRaises(expected_exception=expected_exception):
            parse_intel(form_data=form_data)

        with self.assertRaisesMessage(
            expected_exception=expected_exception, expected_message=expected_message
        ):
            parse_intel(form_data=form_data)


class TestParseIntel(BaseTestCase):
    """
    Test the parse_intel function
    """

    @patch("aa_intel_tool.parser.general.check_intel_type")
    @patch(
        "aa_intel_tool.parser.general.SUPPORTED_INTEL_TYPES",
        {"dscan": {"parser": MagicMock(return_value=MagicMock(hash="hash1"))}},
    )
    def test_parses_valid_dscan_data(self, mock_check_intel_type):
        """
        Test should return the hash of the parsed intel data for valid dscan data

        :param mock_check_intel_type:
        :type mock_check_intel_type:
        :return:
        :rtype:
        """

        mock_check_intel_type.return_value = "dscan"
        form_data = load_dscan_txt()
        result = parse_intel(form_data)

        self.assertEqual(result, "hash1")

    @patch("aa_intel_tool.parser.general.check_intel_type")
    @patch(
        "aa_intel_tool.parser.general.SUPPORTED_INTEL_TYPES",
        {"fleetcomp": {"parser": MagicMock(return_value=MagicMock(hash="hash2"))}},
    )
    def test_parses_valid_fleetcomp_data(self, mock_check_intel_type):
        """
        Test should return the hash of the parsed intel data for valid fleetcomp data

        :param mock_check_intel_type:
        :type mock_check_intel_type:
        :return:
        :rtype:
        """

        mock_check_intel_type.return_value = "fleetcomp"
        form_data = load_fleetcomp_txt()
        result = parse_intel(form_data)

        self.assertEqual(result, "hash2")

    @patch("aa_intel_tool.parser.general.check_intel_type")
    @patch(
        "aa_intel_tool.parser.general.SUPPORTED_INTEL_TYPES",
        {"chatscan": {"parser": MagicMock(return_value=MagicMock(hash="hash3"))}},
    )
    def test_parses_valid_chatscan_data(self, mock_check_intel_type):
        """
        Test should return the hash of the parsed intel data for valid chatscan data

        :param mock_check_intel_type:
        :type mock_check_intel_type:
        :return:
        :rtype:
        """

        mock_check_intel_type.return_value = "chatscan"
        form_data = load_chatscan_txt()
        result = parse_intel(form_data)

        self.assertEqual(result, "hash3")

    @patch("aa_intel_tool.parser.general.check_intel_type")
    def test_raises_error_for_invalid_data(self, mock_check_intel_type):
        """
        Test should throw a ParserError as parsed intel data for invalid data

        :param mock_check_intel_type:
        :type mock_check_intel_type:
        :return:
        :rtype:
        """

        mock_check_intel_type.side_effect = ParserError("Invalid data")
        form_data = load_chatscan_faulty_txt()

        with self.assertRaises(ParserError):
            parse_intel(form_data)

    def test_raises_error_for_empty_data(self):
        """
        Test should throw a ParserError as parsed intel data for empty form data

        :return:
        :rtype:
        """

        form_data = ""

        with self.assertRaises(ParserError):
            parse_intel(form_data)
