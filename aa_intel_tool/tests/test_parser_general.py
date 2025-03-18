"""
Testing the parsers
"""

# Standard Library
from unittest.mock import MagicMock, patch

# Django
from django.test import TestCase

# Alliance Auth (External Libs)
from eveuniverse.models import EveEntity

# AA Intel Tool
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.parser.general import check_intel_type, parse_intel
from aa_intel_tool.parser.module.chatlist import (
    _get_character_info,
    _get_unaffiliated_alliance_info,
    _parse_alliance_info,
    _parse_character_info,
    _parse_chatscan_data,
    _parse_corporation_info,
)
from aa_intel_tool.tests.utils import (
    load_chatscan_faulty_txt,
    load_chatscan_txt,
    load_dscan_txt,
    load_fleetcomp_txt,
)


class TestCheckIntelType(TestCase):
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


class TestParseIntel(TestCase):
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


class TestParseChatScanData(TestCase):
    """
    Test the _parse_chatscan_data function
    """

    @patch("aa_intel_tool.parser.module.chatlist._parse_alliance_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_corporation_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_character_info")
    def test_parses_valid_characters(
        self,
        mock_parse_character_info,
        mock_parse_corporation_info,
        mock_parse_alliance_info,
    ):
        """
        Test should parse valid chatscan data and return a dictionary

        :param mock_parse_character_info:
        :type mock_parse_character_info:
        :param mock_parse_corporation_info:
        :type mock_parse_corporation_info:
        :param mock_parse_alliance_info:
        :type mock_parse_alliance_info:
        :return:
        :rtype:
        """

        eve_characters = MagicMock()
        eve_characters.__iter__.return_value = [
            MagicMock(
                character_name="Character1",
                alliance_name="Alliance1",
                corporation_name="Corp1",
            ),
            MagicMock(
                character_name="Character2",
                alliance_name="Alliance2",
                corporation_name="Corp2",
            ),
        ]
        mock_parse_character_info.side_effect = lambda eve_character: {
            "name": eve_character.character_name
        }
        mock_parse_corporation_info.side_effect = lambda eve_character: {
            "name": eve_character.corporation_name
        }
        mock_parse_alliance_info.side_effect = lambda eve_character: {
            "name": eve_character.alliance_name
        }

        result = _parse_chatscan_data(eve_characters)

        self.assertEqual(len(result["pilots"]), 2)
        self.assertEqual(len(result["corporations"]), 2)
        self.assertEqual(len(result["alliances"]), 2)

    @patch("aa_intel_tool.parser.module.chatlist._parse_alliance_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_corporation_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_character_info")
    def test_handles_unaffiliated_characters(
        self,
        mock_parse_character_info,
        mock_parse_corporation_info,
        mock_parse_alliance_info,
    ):
        """
        Test should handle unaffiliated characters and return "Unaffiliated" as the alliance name

        :param mock_parse_character_info:
        :type mock_parse_character_info:
        :param mock_parse_corporation_info:
        :type mock_parse_corporation_info:
        :param mock_parse_alliance_info:
        :type mock_parse_alliance_info:
        :return:
        :rtype:
        """

        eve_characters = MagicMock()
        eve_characters.__iter__.return_value = [
            MagicMock(
                character_name="Character1",
                alliance_name=None,
                corporation_name="Corp1",
            )
        ]
        mock_parse_character_info.side_effect = lambda eve_character: {
            "name": eve_character.character_name
        }
        mock_parse_corporation_info.side_effect = lambda eve_character: {
            "name": eve_character.corporation_name
        }
        mock_parse_alliance_info.side_effect = lambda eve_character: {
            "name": "Unaffiliated"
        }

        result = _parse_chatscan_data(eve_characters)

        self.assertEqual(result["alliances"][0]["name"], "Unaffiliated")

    @patch("aa_intel_tool.parser.module.chatlist._parse_alliance_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_corporation_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_character_info")
    def test_counts_characters_correctly(
        self,
        mock_parse_character_info,
        mock_parse_corporation_info,
        mock_parse_alliance_info,
    ):
        """
        Test should count characters correctly and return the correct counts for alliances and corporations

        :param mock_parse_character_info:
        :type mock_parse_character_info:
        :param mock_parse_corporation_info:
        :type mock_parse_corporation_info:
        :param mock_parse_alliance_info:
        :type mock_parse_alliance_info:
        :return:
        :rtype:
        """

        eve_characters = MagicMock()
        eve_characters.__iter__.return_value = [
            MagicMock(
                character_name="Character1",
                alliance_name="Alliance1",
                corporation_name="Corp1",
            ),
            MagicMock(
                character_name="Character2",
                alliance_name="Alliance1",
                corporation_name="Corp1",
            ),
            MagicMock(
                character_name="Character3",
                alliance_name="Alliance2",
                corporation_name="Corp2",
            ),
        ]
        mock_parse_character_info.side_effect = lambda eve_character: {
            "name": eve_character.character_name
        }
        mock_parse_corporation_info.side_effect = lambda eve_character: {
            "name": eve_character.corporation_name
        }
        mock_parse_alliance_info.side_effect = lambda eve_character: {
            "name": eve_character.alliance_name
        }

        result = _parse_chatscan_data(eve_characters)

        self.assertEqual(result["alliances"][0]["count"], 2)
        self.assertEqual(result["corporations"][0]["count"], 2)
        self.assertEqual(result["alliances"][1]["count"], 1)
        self.assertEqual(result["corporations"][1]["count"], 1)


class TestParseCharacterInfo(TestCase):
    """
    Test the _parse_character_info function
    """

    @patch("aa_intel_tool.parser.module.chatlist._parse_alliance_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_corporation_info")
    def test_parses_valid_character_info(
        self, mock_parse_corporation_info, mock_parse_alliance_info
    ):
        """
        Test should parse valid character info and return a dictionary

        :param mock_parse_corporation_info:
        :type mock_parse_corporation_info:
        :param mock_parse_alliance_info:
        :type mock_parse_alliance_info:
        :return:
        :rtype:
        """

        eve_character = MagicMock(
            character_id=123,
            character_name="Character1",
            portrait_url_32="portrait_url",
        )
        mock_parse_corporation_info.return_value = {"name": "Corp1"}
        mock_parse_alliance_info.return_value = {"name": "Alliance1"}

        result = _parse_character_info(eve_character)

        self.assertEqual(result["id"], 123)
        self.assertEqual(result["name"], "Character1")
        self.assertEqual(result["portrait"], "portrait_url")
        self.assertEqual(result["corporation"]["name"], "Corp1")
        self.assertEqual(result["alliance"]["name"], "Alliance1")

    @patch("aa_intel_tool.parser.module.chatlist._parse_alliance_info")
    @patch("aa_intel_tool.parser.module.chatlist._parse_corporation_info")
    def test_handles_missing_alliance_info(
        self, mock_parse_corporation_info, mock_parse_alliance_info
    ):
        """
        Test should handle missing alliance info and return "Unaffiliated" as the alliance name

        :param mock_parse_corporation_info:
        :type mock_parse_corporation_info:
        :param mock_parse_alliance_info:
        :type mock_parse_alliance_info:
        :return:
        :rtype:
        """

        eve_character = MagicMock(
            character_id=123,
            character_name="Character1",
            portrait_url_32="portrait_url",
        )
        mock_parse_corporation_info.return_value = {"name": "Corp1"}
        mock_parse_alliance_info.return_value = {"name": "Unaffiliated"}

        result = _parse_character_info(eve_character)

        self.assertEqual(result["alliance"]["name"], "Unaffiliated")


class TestParseCorporationInfo(TestCase):
    """
    Test the _parse_corporation_info function
    """

    @patch("aa_intel_tool.parser.module.chatlist._parse_alliance_info")
    def test_parses_valid_corporation_info(self, mock_parse_alliance_info):
        """
        Test should parse valid corporation info and return a dictionary

        :param mock_parse_alliance_info:
        :type mock_parse_alliance_info:
        :return:
        :rtype:
        """

        eve_character = MagicMock(
            corporation_id=456,
            corporation_name="Corp1",
            corporation_ticker="C1",
            corporation_logo_url_32="corp_logo_url",
        )
        mock_parse_alliance_info.return_value = {"name": "Alliance1"}

        result = _parse_corporation_info(eve_character)

        self.assertEqual(result["id"], 456)
        self.assertEqual(result["name"], "Corp1")
        self.assertEqual(result["ticker"], "C1")
        self.assertEqual(result["logo"], "corp_logo_url")
        self.assertEqual(result["alliance"]["name"], "Alliance1")

    @patch("aa_intel_tool.parser.module.chatlist._parse_alliance_info")
    def test_handles_missing_alliance_info(self, mock_parse_alliance_info):
        """
        Test should handle missing alliance info and return "Unaffiliated" as the alliance name

        :param mock_parse_alliance_info:
        :type mock_parse_alliance_info:
        :return:
        :rtype:
        """

        eve_character = MagicMock(
            corporation_id=456,
            corporation_name="Corp1",
            corporation_ticker="C1",
            corporation_logo_url_32="corp_logo_url",
        )
        mock_parse_alliance_info.return_value = {"name": "Unaffiliated"}

        result = _parse_corporation_info(eve_character, with_alliance_info=False)

        self.assertNotIn("alliance", result)


class TestParseAllianceInfo(TestCase):
    """
    Test the _parse_alliance_info function
    """

    def test_parses_valid_alliance_info(self):
        """
        Test should parse valid alliance info and return a dictionary

        :return:
        :rtype:
        """

        eve_character = MagicMock(
            alliance_id=789,
            alliance_name="Alliance1",
            alliance_ticker="A1",
            alliance_logo_url_32="alliance_logo_url",
        )

        result = _parse_alliance_info(eve_character)

        self.assertEqual(result["id"], 789)
        self.assertEqual(result["name"], "Alliance1")
        self.assertEqual(result["ticker"], "A1")
        self.assertEqual(result["logo"], "alliance_logo_url")
        self.assertIn("dotlan", result)
        self.assertIn("zkillboard", result)

    def test_handles_unaffiliated_alliance(self):
        """
        Test should handle unaffiliated alliance info and return "Unaffiliated" as the alliance name

        :return:
        :rtype:
        """

        eve_character = MagicMock(alliance_id=None)

        result = _parse_alliance_info(eve_character)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "")
        self.assertEqual(result["ticker"], "")
        self.assertIn("logo", result)

    @patch("aa_intel_tool.parser.module.chatlist.dotlan.alliance_url")
    @patch("aa_intel_tool.parser.module.chatlist.zkillboard.alliance_url")
    def test_includes_evelinks(self, mock_zkillboard, mock_dotlan):
        """
        Test should include zkillboard and dotlan links in the result

        :param mock_zkillboard:
        :type mock_zkillboard:
        :param mock_dotlan:
        :type mock_dotlan:
        :return:
        :rtype:
        """

        eve_character = MagicMock(
            alliance_id=789,
            alliance_name="Alliance1",
            alliance_ticker="A1",
            alliance_logo_url_32="alliance_logo_url",
        )
        mock_dotlan.return_value = "dotlan_url"
        mock_zkillboard.return_value = "zkillboard_url"

        result = _parse_alliance_info(eve_character, with_evelinks=True)

        self.assertEqual(result["dotlan"], "dotlan_url")
        self.assertEqual(result["zkillboard"], "zkillboard_url")

    def test_excludes_evelinks(self):
        """
        Test should exclude zkillboard and dotlan links from the result

        :return:
        :rtype:
        """

        eve_character = MagicMock(
            alliance_id=789,
            alliance_name="Alliance1",
            alliance_ticker="A1",
            alliance_logo_url_32="alliance_logo_url",
        )

        result = _parse_alliance_info(eve_character, with_evelinks=False)

        self.assertNotIn("dotlan", result)
        self.assertNotIn("zkillboard", result)


class TestGetUnaffiliatedAllianceInfo(TestCase):
    """
    Test the _get_unaffiliated_alliance_info function
    """

    @patch("aa_intel_tool.parser.module.chatlist.eveimageserver.alliance_logo_url")
    def test_returns_correct_alliance_info(self, mock_alliance_logo_url):
        """
        Test should return the correct information for the unaffiliated alliance

        :param mock_alliance_logo_url:
        :type mock_alliance_logo_url:
        :return:
        :rtype:
        """

        mock_alliance_logo_url.return_value = "mock_logo_url"

        result = _get_unaffiliated_alliance_info()

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "")
        self.assertEqual(result["ticker"], "")
        self.assertEqual(result["logo"], "mock_logo_url")

    @patch("aa_intel_tool.parser.module.chatlist.eveimageserver.alliance_logo_url")
    def handles_logo_url_generation(self, mock_alliance_logo_url):
        """
        Test should generate the correct logo URL for the unaffiliated alliance

        :param mock_alliance_logo_url:
        :type mock_alliance_logo_url:
        :return:
        :rtype:
        """

        mock_alliance_logo_url.return_value = "mock_logo_url"

        result = _get_unaffiliated_alliance_info()

        mock_alliance_logo_url.assert_called_once_with(alliance_id=1, size=32)
        self.assertEqual(result["logo"], "mock_logo_url")


class TestGetCharacterInfo(TestCase):
    """
    Test the _get_character_info function
    """

    @patch("aa_intel_tool.parser.module.chatlist.EveCharacter.objects.filter")
    @patch("aa_intel_tool.parser.module.chatlist.get_or_create_character")
    def test_returns_existing_characters(self, mock_get_or_create, mock_filter):
        """
        Test should return existing characters from the database

        :param mock_get_or_create:
        :type mock_get_or_create:
        :param mock_filter:
        :type mock_filter:
        :return:
        :rtype:
        """

        # Mock the QuerySet returned by filter
        mock_queryset = MagicMock()
        mock_queryset.exclude.return_value = mock_queryset
        mock_queryset.count.return_value = 0
        mock_queryset.__iter__.return_value = iter([])
        mock_filter.return_value = mock_queryset

        # Mock the creation of a new character
        mock_get_or_create.return_value = [MagicMock(character_name="Character1")]

        result = _get_character_info(["Character1", "Character2"])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].character_name, "Character1")

    @patch("aa_intel_tool.parser.module.chatlist.EveCharacter.objects.filter")
    def test_fetches_characters_from_eveuniverse(self, mock_filter):
        """
        Test should fetch characters from the Eve Universe API

        :param mock_filter:
        :type mock_filter:
        :return:
        :rtype:
        """

        mock_filter.return_value.exclude.return_value.count.return_value = 0

        with patch(
            "aa_intel_tool.parser.module.chatlist.EveEntity.objects.fetch_by_names_esi"
        ) as mock_fetch:
            mock_fetch.return_value.filter.return_value.values_list.return_value = [1]
            with patch(
                "aa_intel_tool.parser.module.chatlist.get_or_create_character"
            ) as mock_get_or_create:
                mock_get_or_create.return_value = [
                    MagicMock(character_name="Character1")
                ]

                result = _get_character_info(["Character1"])

                self.assertEqual(len(result), 1)
                self.assertEqual(result[0].character_name, "Character1")

    @patch("aa_intel_tool.parser.module.chatlist.EveCharacter.objects.filter")
    def test_handles_no_characters_found(self, mock_filter):
        """
        Test should raise a ParserError when no characters are found

        :param mock_filter:
        :type mock_filter:
        :return:
        :rtype:
        """

        mock_filter.return_value.exclude.return_value.count.return_value = 0

        with patch(
            "aa_intel_tool.parser.module.chatlist.EveEntity.objects.fetch_by_names_esi"
        ) as mock_fetch:
            mock_fetch.return_value.filter.return_value.values_list.return_value = []
            with self.assertRaises(ParserError):
                _get_character_info(["UnknownCharacter"])

    @patch("aa_intel_tool.parser.module.chatlist.EveCharacter.objects.filter")
    def test_handles_eveuniverse_fetch_error(self, mock_filter):
        """
        Test should raise a ParserError when there is an error fetching from the Eve Universe API

        :param mock_filter:
        :type mock_filter:
        :return:
        :rtype:
        """

        mock_filter.return_value.exclude.return_value.count.return_value = 0

        with patch(
            "aa_intel_tool.parser.module.chatlist.EveEntity.objects.fetch_by_names_esi"
        ) as mock_fetch:
            mock_fetch.side_effect = EveEntity.DoesNotExist
            with self.assertRaises(ParserError):
                _get_character_info(["Character1"])
