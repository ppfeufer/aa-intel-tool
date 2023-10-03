"""
Testing the parsers
"""

# Django
from django.test import TestCase

# AA Intel Tool
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.parser.general import check_intel_type, parse_intel
from aa_intel_tool.tests.utils import (
    load_chatscan_faulty_txt,
    load_chatscan_txt,
    load_dscan_txt,
    load_fleetcomp_txt,
)


class TestParserGeneral(TestCase):
    """
    Testing parser.general.py
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
        expected_message = "A parser error occurred » No suitable parser found. Input is not a supported intel type or malformed …"  # pylint: disable=line-too-long

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
        expected_message = "A parser error occurred » No suitable parser found. Input is not a supported intel type or malformed …"  # pylint: disable=line-too-long

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
