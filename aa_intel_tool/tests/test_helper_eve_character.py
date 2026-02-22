"""
Tests for the helper functions in the eve_character module.
"""

# Standard Library
from types import SimpleNamespace
from unittest.mock import Mock, patch

# Alliance Auth
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCorporationInfo,
)

# AA Intel Tool
from aa_intel_tool.helper.eve_character import (
    _create_alliance,
    _create_corporation,
    _fetch_affiliations_with_retry,
    _fetch_ids_with_retry,
    _get_alliance_info_from_affiliation,
    _get_corporation_info_from_affiliation,
    create_characters,
    fetch_character_ids_from_esi,
    temp_alliance_data,
    temp_corp_data,
)
from aa_intel_tool.providers import ESIHandler
from aa_intel_tool.tests import BaseTestCase


class TestCreateAlliance(BaseTestCase):
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


class TestCreateCorporation(BaseTestCase):
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


class TestGetCorporationInfoFromAffiliation(BaseTestCase):
    """
    Test the _get_corporation_info_from_affiliation function.
    """

    def test_retrieves_corporation_info_from_cache(self):
        """
        Test that corporation information is retrieved from the cache when available.

        :return:
        :rtype:
        """

        temp_corp_data[12345] = {"corporation_id": 12345, "name": "Cached Corporation"}
        affiliation_data = {"corporation_id": 12345}

        result = _get_corporation_info_from_affiliation(affiliation_data)

        self.assertEqual(
            result, {"corporation_id": 12345, "name": "Cached Corporation"}
        )
        self.assertIn(12345, temp_corp_data)

    def test_fetches_corporation_info_when_not_in_cache(self):
        """
        Test that corporation information is fetched from the ESI API when not available in the cache.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "get_corporations_corporation_id",
            return_value={"corporation_id": 67890, "name": "Fetched Corporation"},
        ) as mock_fetch:
            affiliation_data = {"corporation_id": 67890}

            result = _get_corporation_info_from_affiliation(affiliation_data)

            self.assertEqual(
                result, {"corporation_id": 67890, "name": "Fetched Corporation"}
            )
            self.assertIn(67890, temp_corp_data)
            mock_fetch.assert_called_once_with(corporation_id=67890, use_etag=False)

    def test_returns_none_when_corporation_id_is_invalid(self):
        """
        Test that None is returned when the corporation ID is invalid and cannot be fetched.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler, "get_corporations_corporation_id", return_value=None
        ) as mock_fetch:
            affiliation_data = {"corporation_id": 99999}

            result = _get_corporation_info_from_affiliation(affiliation_data)

            self.assertIsNone(result)
            self.assertIn(99999, temp_corp_data)
            mock_fetch.assert_called_once_with(corporation_id=99999, use_etag=False)


class TestGetAllianceInfofromAffiliation(BaseTestCase):
    """
    Test the _get_alliance_info_from_affiliation function.
    """

    def test_retrieves_alliance_info_from_cache(self):
        """
        Test that alliance information is retrieved from the cache when available.

        :return:
        :rtype:
        """

        temp_alliance_data[54321] = {"alliance_id": 54321, "name": "Cached Alliance"}
        affiliation_data = {"alliance_id": 54321, "character_id": 12345}

        result = _get_alliance_info_from_affiliation(affiliation_data)

        self.assertEqual(result, {"alliance_id": 54321, "name": "Cached Alliance"})
        self.assertIn(54321, temp_alliance_data)

    def test_fetches_alliance_info_when_not_in_cache(self):
        """
        Test that alliance information is fetched from the ESI API when not available in the cache.

        :return:
        :rtype:

        """
        with patch.object(
            ESIHandler,
            "get_alliances_alliance_id",
            return_value={"alliance_id": 98765, "name": "Fetched Alliance"},
        ) as mock_fetch:
            affiliation_data = {"alliance_id": 98765, "character_id": 12345}

            result = _get_alliance_info_from_affiliation(affiliation_data)

            self.assertEqual(result, {"alliance_id": 98765, "name": "Fetched Alliance"})
            self.assertIn(98765, temp_alliance_data)
            mock_fetch.assert_called_once_with(alliance_id=98765, use_etag=False)

    def test_returns_none_when_alliance_id_is_missing(self):
        """
        Test that None is returned when the alliance ID is missing from the affiliation data.

        :return:
        :rtype:
        """

        affiliation_data = {"character_id": 12345}

        result = _get_alliance_info_from_affiliation(affiliation_data)

        self.assertIsNone(result)


class TestFetchAffiliationsWithRetry(BaseTestCase):
    """
    Test the _fetch_affiliations_with_retry function.
    """

    def test_returns_affiliations_for_valid_chunk(self):
        """
        Test that affiliations are returned for a valid chunk of character IDs.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "post_characters_affiliation",
            return_value=[
                {"character_id": 1, "corporation_id": 100, "alliance_id": 200}
            ],
        ) as mock_post:
            result = _fetch_affiliations_with_retry(chunk=[1])

            self.assertEqual(
                result, [{"character_id": 1, "corporation_id": 100, "alliance_id": 200}]
            )

            mock_post.assert_called_once_with(ids=[1])

    def test_handles_empty_chunk_gracefully(self):
        """
        Test that an empty chunk is handled gracefully and returns an empty list.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler, "post_characters_affiliation", return_value=[]
        ) as mock_post:
            result = _fetch_affiliations_with_retry(chunk=[])

            self.assertEqual(result, [])

            mock_post.assert_called_once_with(ids=[])

    def test_retries_on_exception_and_returns_combined_results(self):
        """
        Test that the function retries on an exception and returns combined results from multiple attempts.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "post_characters_affiliation",
            side_effect=[
                Exception("ESI error"),
                [{"character_id": 2}],
                [{"character_id": 3}],
            ],
        ) as mock_post:
            result = _fetch_affiliations_with_retry(chunk=[1, 2, 3])

            self.assertEqual(result, [{"character_id": 2}, {"character_id": 3}])
            self.assertEqual(mock_post.call_count, 3)

    def test_ignores_single_character_on_failure(self):
        """
        Test that the function ignores a single character ID on failure and returns an empty list.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "post_characters_affiliation",
            side_effect=Exception("ESI error"),
        ) as mock_post:
            result = _fetch_affiliations_with_retry(chunk=[1])

            self.assertEqual(result, [])

            mock_post.assert_called_once_with(ids=[1])


class TestFetchIdsWithRetry(BaseTestCase):
    """
    Test the _fetch_ids_with_retry function.
    """

    def test_returns_ids_for_valid_chunk(self):
        """
        Test that IDs are returned for a valid chunk of names.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler, "post_universe_ids", return_value=[{"id": 1, "name": "Test"}]
        ) as mock_post:
            result = _fetch_ids_with_retry(chunk=["Test"])

            self.assertEqual(result, [{"id": 1, "name": "Test"}])

            mock_post.assert_called_once_with(names=["Test"])

    def test_handles_empty_chunk_gracefully(self):
        """
        Test that an empty chunk is handled gracefully and returns an empty list.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler, "post_universe_ids", return_value=[]
        ) as mock_post:
            result = _fetch_ids_with_retry(chunk=[])

            self.assertEqual(result, [])

            mock_post.assert_called_once_with(names=[])

    def test_retries_on_exception_and_returns_combined_results(self):
        """
        Test that the function retries on an exception and returns combined results from multiple attempts.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "post_universe_ids",
            side_effect=[Exception("ESI error"), [{"id": 2}], [{"id": 3}]],
        ) as mock_post:
            result = _fetch_ids_with_retry(chunk=["A", "B", "C"])

            self.assertEqual(result, [{"id": 2}, {"id": 3}])
            self.assertEqual(mock_post.call_count, 3)

    def test_ignores_single_name_on_failure(self):
        """
        Test that the function ignores a single name on failure and returns an empty list.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler, "post_universe_ids", side_effect=Exception("ESI error")
        ) as mock_post:
            result = _fetch_ids_with_retry(chunk=["Test"])

            self.assertEqual(result, [])

            mock_post.assert_called_once_with(names=["Test"])


class TestCreateCharacters(BaseTestCase):
    """
    Test the create_characters function.
    """

    def test_creates_characters_with_affiliations(self):
        """
        Test that characters are created with their affiliations when with_affiliation is True.

        :return:
        :rtype:
        """

        character_data = [
            SimpleNamespace(id=1, name="Character One"),
            SimpleNamespace(id=2, name="Character Two"),
        ]
        affiliations = [
            SimpleNamespace(
                character_id=1,
                character_name="Character One",
                corporation_id=100,
                alliance_id=200,
                faction_id=None,
            ),
            SimpleNamespace(
                character_id=2,
                character_name="Character Two",
                corporation_id=101,
                alliance_id=None,
                faction_id=None,
            ),
        ]

        with (
            patch(
                "aa_intel_tool.helper.eve_character._fetch_affiliations_with_retry",
                return_value=affiliations,
            ),
            patch(
                "aa_intel_tool.helper.eve_character._create_alliance"
            ) as mock_create_alliance,
            patch(
                "aa_intel_tool.helper.eve_character._create_corporation"
            ) as mock_create_corporation,
            patch.object(
                ESIHandler,
                "get_corporations_corporation_id",
                side_effect=lambda corporation_id, use_etag=False: SimpleNamespace(
                    corporation_id=corporation_id,
                    name=f"Corp {corporation_id}",
                    ticker=f"C{corporation_id}",
                ),
            ),
            patch.object(
                ESIHandler,
                "get_alliances_alliance_id",
                side_effect=lambda alliance_id, use_etag=False: SimpleNamespace(
                    alliance_id=alliance_id,
                    name=f"All {alliance_id}",
                    ticker=f"A{alliance_id}",
                ),
            ),
            patch.object(ESIHandler, "get_universe_factions", return_value=[]),
        ):
            result = create_characters(character_data, with_affiliation=True)

            # allow actual bulk_create to run and return a queryset we can count
            self.assertEqual(result.count(), 2)
            mock_create_alliance.assert_called_once_with({200})
            mock_create_corporation.assert_called_once_with({101})

    def test_handles_empty_character_data(self):
        """
        Test that the function handles empty character data gracefully and does not attempt to create any characters or affiliations.

        :return:
        :rtype:
        """

        with (
            patch(
                "aa_intel_tool.helper.eve_character.EveCharacter.objects.bulk_create"
            ) as mock_bulk_create,
            patch.object(ESIHandler, "get_universe_factions", return_value=[]),
        ):
            result = create_characters([], with_affiliation=True)

            mock_bulk_create.assert_not_called()
            self.assertEqual(result.count(), 0)

    def test_skips_affiliation_creation_when_disabled(self):
        """
        Test that the function skips affiliation creation when with_affiliation is False, and does not create any alliances or corporations.

        :return:
        :rtype:
        """

        character_data = [
            Mock(id=1, name="Character One"),
        ]
        affiliations = [
            SimpleNamespace(
                character_id=1,
                character_name="Character One",
                corporation_id=100,
                alliance_id=200,
                faction_id=None,
            ),
        ]

        with (
            patch(
                "aa_intel_tool.helper.eve_character._fetch_affiliations_with_retry",
                return_value=affiliations,
            ),
            patch(
                "aa_intel_tool.helper.eve_character.EveCharacter.objects.bulk_create"
            ) as mock_bulk_create,
            patch(
                "aa_intel_tool.helper.eve_character._create_alliance"
            ) as mock_create_alliance,
            patch(
                "aa_intel_tool.helper.eve_character._create_corporation"
            ) as mock_create_corporation,
            patch.object(ESIHandler, "get_universe_factions", return_value=[]),
        ):
            result = create_characters(character_data, with_affiliation=False)

            # Ensure bulk_create was called once, then safely inspect the first arg
            mock_bulk_create.assert_called_once()
            created_arg = (
                mock_bulk_create.call_args[0][0] if mock_bulk_create.call_args else None
            )
            self.assertIsNotNone(created_arg)
            self.assertIsInstance(created_arg, list)
            self.assertEqual(len(created_arg), 1)

            mock_create_alliance.assert_not_called()
            mock_create_corporation.assert_not_called()
            self.assertEqual(result.count(), 0)


class TestFetchCharacterIdsFromEsi(BaseTestCase):
    """
    Test the fetch_character_ids_from_esi function.
    """

    def test_fetches_character_ids_in_chunks(self):
        """
        Test that character IDs are fetched in chunks of 400 and combined correctly.

        :return:
        :rtype:
        """

        characters_to_fetch = {f"Character {i}" for i in range(1200)}
        per_call = [f"ID {i}" for i in range(400)]
        esi_response = SimpleNamespace(characters=per_call)

        with patch(
            "aa_intel_tool.helper.eve_character._fetch_ids_with_retry",
            return_value=esi_response,
        ) as mock_fetch_ids_with_retry:
            result = fetch_character_ids_from_esi(characters_to_fetch)

            self.assertEqual(len(result), 1200)
            self.assertEqual(mock_fetch_ids_with_retry.call_count, 3)
            self.assertEqual(result[:400], per_call)

    def test_handles_empty_input_gracefully(self):
        """
        Test that an empty set of character names is handled gracefully and returns an empty list without making any API calls.

        :return:
        :rtype:
        """

        characters_to_fetch = set()

        with patch(
            "aa_intel_tool.helper.eve_character._fetch_ids_with_retry"
        ) as mock_fetch_ids_with_retry:
            result = fetch_character_ids_from_esi(characters_to_fetch)

            self.assertEqual(result, [])
            mock_fetch_ids_with_retry.assert_not_called()

    def test_handles_partial_failures_gracefully(self):
        """
        Test that if one chunk fails to fetch IDs, the function continues to fetch remaining chunks and combines results correctly.

        :return:
        :rtype:
        """

        characters_to_fetch = {"Character 1", "Character 2"}
        esi_response = SimpleNamespace(characters=["ID 1"])

        with patch(
            "aa_intel_tool.helper.eve_character._fetch_ids_with_retry",
            side_effect=[esi_response, []],
        ) as mock_fetch_ids_with_retry:
            result = fetch_character_ids_from_esi(characters_to_fetch)

            self.assertEqual(result, ["ID 1"])
            self.assertEqual(mock_fetch_ids_with_retry.call_count, 1)

    def test_handles_large_chunks_correctly(self):
        """
        Test that if the number of character names exceeds the chunk size, the function correctly processes multiple chunks and combines results.

        :return:
        :rtype:
        """

        characters_to_fetch = {f"Character {i}" for i in range(500)}
        esi_response = SimpleNamespace(characters=[f"ID {i}" for i in range(500)])

        with patch(
            "aa_intel_tool.helper.eve_character._fetch_ids_with_retry",
            return_value=esi_response,
        ) as mock_fetch_ids_with_retry:
            result = fetch_character_ids_from_esi(characters_to_fetch)

            self.assertEqual(len(result), 500)
            self.assertEqual(result, esi_response.characters)
            mock_fetch_ids_with_retry.assert_called_once()
