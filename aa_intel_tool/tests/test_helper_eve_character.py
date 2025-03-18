"""
Tests for the helper functions in the eve_character module.
"""

# Standard Library
from unittest.mock import Mock, patch

# Django
from django.test import TestCase

# Alliance Auth
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)

# AA Intel Tool
from aa_intel_tool.helper.eve_character import (
    _create_alliance,
    _create_character,
    _create_corporation,
    get_or_create_character,
)


class TestCreateAlliance(TestCase):
    """
    Test the _create_alliance function.
    """

    def test_creates_new_alliances(self):
        """
        Test that new alliances are created when they do not exist in the database.

        :return:
        :rtype:
        """

        alliance_ids = [1001, 1002, 1003]

        with (
            patch.object(
                EveAllianceInfo.objects,
                "filter",
                return_value=EveAllianceInfo.objects.none(),
            ),
            patch.object(
                EveAllianceInfo.objects, "create_alliance"
            ) as mock_create_alliance,
        ):
            _create_alliance(alliance_ids)

            self.assertEqual(mock_create_alliance.call_count, 3)

    def test_does_not_create_existing_alliances(self):
        """
        Test that existing alliances are not created again.

        :return:
        :rtype:
        """

        alliance_ids = [1001, 1002, 1003]

        # Create existing alliances in the database
        EveAllianceInfo.objects.create(
            alliance_id=1001, alliance_name="Alliance 1001", executor_corp_id=2001
        )
        EveAllianceInfo.objects.create(
            alliance_id=1002, alliance_name="Alliance 1002", executor_corp_id=2002
        )

        with (
            patch.object(
                EveAllianceInfo.objects,
                "filter",
                wraps=EveAllianceInfo.objects.filter,
            ),
            patch.object(
                EveAllianceInfo.objects, "create_alliance"
            ) as mock_create_alliance,
        ):
            _create_alliance(alliance_ids)

            mock_create_alliance.assert_called_once_with(alliance_id=1003)

    def test_handles_empty_alliance_ids(self):
        """
        Test that no alliances are created when the input list is empty.

        :return:
        :rtype:
        """

        alliance_ids = []

        with (
            patch.object(EveAllianceInfo.objects, "filter"),
            patch.object(
                EveAllianceInfo.objects, "create_alliance"
            ) as mock_create_alliance,
        ):
            _create_alliance(alliance_ids)

            mock_create_alliance.assert_not_called()


class TestCreateCorporation(TestCase):
    """
    Test the _create_corporation function.
    """

    def test_creates_new_corporations(self):
        """
        Test that new corporations are created when they do not exist in the database.

        :return:
        :rtype:
        """

        corporation_ids = [2001, 2002, 2003]

        with (
            patch.object(
                EveCorporationInfo.objects,
                "filter",
                return_value=EveCorporationInfo.objects.none(),
            ),
            patch.object(
                EveCorporationInfo.objects, "create_corporation"
            ) as mock_create_corporation,
        ):
            _create_corporation(corporation_ids)

            self.assertEqual(mock_create_corporation.call_count, 3)

    def test_does_not_create_existing_corporations(self):
        """
        Test that existing corporations are not created again.

        :return:
        :rtype:
        """

        corporation_ids = [2001, 2002, 2003]

        EveCorporationInfo.objects.create(
            corporation_id=2001, corporation_name="Corporation 2001", member_count=10
        )
        EveCorporationInfo.objects.create(
            corporation_id=2002, corporation_name="Corporation 2002", member_count=20
        )

        with (
            patch.object(
                EveCorporationInfo.objects,
                "filter",
                wraps=EveCorporationInfo.objects.filter,
            ),
            patch.object(
                EveCorporationInfo.objects, "create_corporation"
            ) as mock_create_corporation,
        ):
            _create_corporation(corporation_ids)

            mock_create_corporation.assert_called_once_with(corp_id=2003)

    def test_handles_empty_corporation_ids(self):
        """
        Test that no corporations are created when the input list is empty.

        :return:
        :rtype:
        """

        corporation_ids = []

        with (
            patch.object(EveCorporationInfo.objects, "filter"),
            patch.object(
                EveCorporationInfo.objects, "create_corporation"
            ) as mock_create_corporation,
        ):
            _create_corporation(corporation_ids)

            mock_create_corporation.assert_not_called()


class TestCreateCharacter(TestCase):
    """
    Test the _create_character function.
    """

    @patch("aa_intel_tool.helper.eve_character.EveCharacter.objects.create_character")
    @patch("aa_intel_tool.helper.eve_character.EveAllianceInfo.objects.create_alliance")
    @patch("allianceauth.eveonline.providers.provider.get_corp")
    def test_creates_new_characters(
        self, mock_get_corp, mock_create_alliance, mock_create_character
    ):
        # Setup mock return values
        mock_create_character.side_effect = [
            Mock(character_id=1001, alliance_id=3001, corporation_id=2001),
            Mock(character_id=1002, alliance_id=3001, corporation_id=2002),
            Mock(character_id=1003, alliance_id=None, corporation_id=2003),
        ]

        mock_get_corp_side_effect = [
            Mock(
                id=2001,
                name="Corporation 2001",
                ticker="TICK1",
                alliance_id=3001,
                members=10,
            ),
            Mock(
                id=2002,
                name="Corporation 2002",
                ticker="TICK2",
                alliance_id=3001,
                members=20,
            ),
            Mock(
                id=2003,
                name="Corporation 2003",
                ticker="TICK3",
                alliance_id=None,
                members=30,
            ),
        ]

        # Ensure the mock objects return plain values for attributes
        for mock_corp in mock_get_corp_side_effect:
            mock_corp.name = "Corporation " + str(mock_corp.id)
            mock_corp.ticker = "TICK" + str(mock_corp.id % 1000)
            mock_corp.members = mock_corp.members

        mock_get_corp.side_effect = (
            lambda *args, **kwargs: mock_get_corp_side_effect.pop(0)
        )

        # Call the function under test
        _create_character(character_ids=[1, 2, 3], with_affiliation=True)

        # Assert that create_character was called three times
        self.assertEqual(mock_create_character.call_count, 3)

        # Assert that create_alliance was called once with the correct ID
        mock_create_alliance.assert_called_once_with(alliance_id=3001)

    def test_handles_empty_character_ids(self):
        """
        Test that no characters are created when the input list is empty.

        :return:
        :rtype:
        """

        character_ids = []

        with (
            patch.object(EveCharacter.objects, "filter"),
            patch.object(
                EveCharacter.objects, "create_character"
            ) as mock_create_character,
        ):
            _create_character(character_ids)

            mock_create_character.assert_not_called()

    @patch("aa_intel_tool.helper.eve_character.EveCharacter.objects.create_character")
    @patch("aa_intel_tool.helper.eve_character.EveAllianceInfo.objects.create_alliance")
    @patch("allianceauth.eveonline.providers.provider.get_corp")
    def creates_characters_without_affiliation(
        self, mock_get_corp, mock_create_alliance, mock_create_character
    ):
        # Setup mock return values
        mock_create_character.side_effect = [
            Mock(character_id=1001, alliance_id=3001, corporation_id=2001),
            Mock(character_id=1002, alliance_id=3001, corporation_id=2002),
            Mock(character_id=1003, alliance_id=None, corporation_id=2003),
        ]

        mock_get_corp_side_effect = [
            Mock(
                id=2001,
                name="Corporation 2001",
                ticker="TICK1",
                alliance_id=3001,
                members=10,
            ),
            Mock(
                id=2002,
                name="Corporation 2002",
                ticker="TICK2",
                alliance_id=3001,
                members=20,
            ),
            Mock(
                id=2003,
                name="Corporation 2003",
                ticker="TICK3",
                alliance_id=None,
                members=30,
            ),
        ]

        # Ensure the mock objects return plain values for attributes
        for mock_corp in mock_get_corp_side_effect:
            mock_corp.name = "Corporation " + str(mock_corp.id)
            mock_corp.ticker = "TICK" + str(mock_corp.id % 1000)
            mock_corp.members = mock_corp.members

        mock_get_corp.side_effect = (
            lambda *args, **kwargs: mock_get_corp_side_effect.pop(0)
        )

        # Call the function under test
        _create_character(character_ids=[1, 2, 3], with_affiliation=False)

        # Assert that create_character was called three times
        self.assertEqual(mock_create_character.call_count, 3)

        # Assert that create_alliance was called once with the correct ID
        mock_create_alliance.assert_called_once_with(alliance_id=3001)


class TestGetOrCreateCharacter(TestCase):
    """
    Test the get_or_create_character function.
    """

    @patch("aa_intel_tool.helper.eve_character._create_character")
    def test_returns_existing_characters(self, mock_create_character):
        """
        Test that existing characters are returned without creating new ones.

        :param mock_create_character:
        :type mock_create_character:
        :return:
        :rtype:
        """

        character_ids = [3001, 3002]
        EveCharacter.objects.create(
            character_id=3001,
            character_name="Character 3001",
            corporation_id=2001,
            alliance_id=1001,
        )
        EveCharacter.objects.create(
            character_id=3002,
            character_name="Character 3002",
            corporation_id=2002,
            alliance_id=1002,
        )

        characters = get_or_create_character(character_ids)

        self.assertEqual(characters.count(), 2)
        mock_create_character.assert_not_called()

    @patch("aa_intel_tool.helper.eve_character._create_character")
    def test_creates_missing_characters(self, mock_create_character):
        """
        Test that missing characters are created when they do not exist in the database.

        :param mock_create_character:
        :type mock_create_character:
        :return:
        :rtype:
        """

        character_ids = [3001, 3002, 3003]
        EveCharacter.objects.create(
            character_id=3001,
            character_name="Character 3001",
            corporation_id=2001,
            alliance_id=1001,
        )

        characters = get_or_create_character(character_ids)

        self.assertEqual(characters.count(), 1)
        mock_create_character.assert_called_once_with(
            character_ids={3002, 3003}, with_affiliation=True
        )

    @patch("aa_intel_tool.helper.eve_character._create_character")
    def handles_empty_character_ids(self, mock_create_character):
        character_ids = []

        characters = get_or_create_character(character_ids)

        self.assertEqual(characters.count(), 0)
        mock_create_character.assert_not_called()

    @patch("aa_intel_tool.helper.eve_character._create_character")
    def handles_none_character_ids(self, mock_create_character):
        character_ids = None

        characters = get_or_create_character(character_ids)

        self.assertEqual(characters.count(), 0)
        mock_create_character.assert_not_called()
