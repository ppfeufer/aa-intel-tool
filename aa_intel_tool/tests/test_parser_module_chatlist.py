"""
Test cases for the chatlist parser module.
"""

# Standard Library
from unittest.mock import MagicMock, patch

# AA Intel Tool
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.models import Scan
from aa_intel_tool.parser.module.chatlist import (
    _get_character_info,
    _get_unaffiliated_alliance_info,
    _parse_alliance_info,
    _parse_character_info,
    _parse_chatscan_data,
    _parse_corporation_info,
    parse,
)
from aa_intel_tool.tests import BaseTestCase


class TestParse(BaseTestCase):
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


class TestParseChatScanData(BaseTestCase):
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


class TestParseCharacterInfo(BaseTestCase):
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


class TestParseCorporationInfo(BaseTestCase):
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

    def test_excludes_alliance_info_when_not_requested(self):
        """
        Test should exclude alliance info from the result when with_alliance_info is False

        :return:
        :rtype:
        """

        eve_character = MagicMock(
            corporation_id=456,
            corporation_name="Corp1",
            corporation_ticker="C1",
            corporation_logo_url_32="corp_logo_url",
        )

        result = _parse_corporation_info(eve_character, with_evelinks=False)

        self.assertNotIn("dotlan", result)
        self.assertNotIn("zkillboard", result)


class TestParseAllianceInfo(BaseTestCase):
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


class TestGetUnaffiliatedAllianceInfo(BaseTestCase):
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


class TestGetCharacterInfo(BaseTestCase):
    """
    Test the _get_character_info function
    """

    def test_returns_all_characters_when_all_are_in_database(self):
        """
        Test should return all characters from the database when they are all present

        :return:
        :rtype:
        """

        scan_data = ["Character 1", "Character 2"]

        eve_characters = MagicMock()
        eve_characters.count.return_value = len(scan_data)
        eve_characters.__len__.return_value = len(scan_data)
        eve_characters.values_list.side_effect = lambda *args, **kwargs: (
            list(scan_data) if kwargs.get("flat") else [(n,) for n in scan_data]
        )

        filter_qs = MagicMock()
        filter_qs.exclude.return_value = eve_characters

        with (
            patch(
                "aa_intel_tool.parser.module.chatlist.EveCharacter.objects.filter",
                return_value=filter_qs,
            ) as mock_filter,
            patch(
                "aa_intel_tool.parser.module.chatlist.fetch_character_ids_from_esi"
            ) as mock_fetch,
        ):
            result = _get_character_info(scan_data)

            mock_filter.assert_called_once_with(character_name__in=scan_data)
            filter_qs.exclude.assert_called_once_with(corporation_id=1000001)
            mock_fetch.assert_not_called()
            self.assertEqual(result, eve_characters)

    def test_fetches_missing_characters_from_esi_when_not_in_database(self):
        """
        Test should fetch missing characters from ESI when they are not present in the database

        :return:
        :rtype:
        """

        scan_data = ["Character 1", "Character 2", "Character 3"]
        existing_characters = ["Character 1", "Character 2"]
        fetched_characters = [{"character_name": "Character 3"}]

        eve_characters = MagicMock()
        eve_characters.count.return_value = len(existing_characters)
        eve_characters.values_list.side_effect = lambda *args, **kwargs: (
            list(existing_characters)
            if kwargs.get("flat")
            else [(n,) for n in existing_characters]
        )

        new_eve_characters = MagicMock()

        filter_qs = MagicMock()
        filter_qs.exclude.return_value = eve_characters

        with (
            patch(
                "aa_intel_tool.parser.module.chatlist.EveCharacter.objects.filter",
                return_value=filter_qs,
            ) as mock_filter,
            patch(
                "aa_intel_tool.parser.module.chatlist.fetch_character_ids_from_esi",
                return_value=fetched_characters,
            ) as mock_fetch,
            patch(
                "aa_intel_tool.parser.module.chatlist.create_characters",
                return_value=new_eve_characters,
            ) as mock_create,
        ):
            result = _get_character_info(scan_data)

            mock_filter.assert_called_once_with(character_name__in=scan_data)
            filter_qs.exclude.assert_called_once_with(corporation_id=1000001)
            mock_fetch.assert_called_once_with(characters_to_fetch={"Character 3"})
            mock_create.assert_called_once_with(
                character_data_from_esi=fetched_characters
            )
            self.assertEqual(result, eve_characters | new_eve_characters)

    def test_does_not_create_characters_when_esi_returns_nothing(self):
        """
        Test should not create characters when ESI returns no data for the missing characters

        :return:
        :rtype:
        """

        scan_data = ["Character 1", "Character 2"]
        existing_characters = ["Character 1"]

        eve_characters = MagicMock()
        eve_characters.count.return_value = len(existing_characters)
        eve_characters.values_list.side_effect = lambda *args, **kwargs: (
            list(existing_characters)
            if kwargs.get("flat")
            else [(n,) for n in existing_characters]
        )

        filter_qs = MagicMock()
        filter_qs.exclude.return_value = eve_characters

        with (
            patch(
                "aa_intel_tool.parser.module.chatlist.EveCharacter.objects.filter",
                return_value=filter_qs,
            ),
            patch(
                "aa_intel_tool.parser.module.chatlist.fetch_character_ids_from_esi",
                return_value=[],
            ) as mock_fetch,
            patch(
                "aa_intel_tool.parser.module.chatlist.create_characters"
            ) as mock_create,
        ):
            result = _get_character_info(scan_data)

            mock_fetch.assert_called_once_with(characters_to_fetch={"Character 2"})
            mock_create.assert_not_called()
            self.assertEqual(result, eve_characters)
