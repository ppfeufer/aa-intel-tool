"""
Tests for the helper functions in the eve_character module.
"""

# Standard Library
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

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

    def test_fetches_ids_successfully(self):
        """
        Test that IDs are fetched successfully for a valid chunk of character names.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "post_universe_ids",
            return_value=SimpleNamespace(
                model_dump=lambda: {"characters": [{"id": 1, "name": "Test"}]}
            ),
        ) as mock_post:
            result = _fetch_ids_with_retry(chunk=["Test"])

            self.assertEqual(result, [{"id": 1, "name": "Test"}])
            mock_post.assert_called_once_with(names=["Test"])

    def test_retries_on_exception_and_combines_results(self):
        """
        Test that the function retries on an exception and returns combined results from multiple attempts.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "post_universe_ids",
            side_effect=[
                Exception("ESI error"),
                SimpleNamespace(
                    model_dump=lambda: {"characters": [{"id": 2, "name": "Test2"}]}
                ),
                SimpleNamespace(
                    model_dump=lambda: {"characters": [{"id": 3, "name": "Test3"}]}
                ),
            ],
        ) as mock_post:
            result = _fetch_ids_with_retry(chunk=["A", "B", "C"])

            self.assertEqual(result, [])
            self.assertEqual(mock_post.call_count, 3)

    def test_handles_empty_chunk_gracefully(self):
        """
        Test that an empty chunk is handled gracefully and returns an empty list.

        :return:
        :rtype:
        """

        result = _fetch_ids_with_retry(chunk=[])

        self.assertEqual(result, [])

    def test_ignores_failed_single_name(self):
        """
        Test that the function ignores a single character name on failure and returns an empty list.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "post_universe_ids",
            side_effect=Exception("ESI error"),
        ) as mock_post:
            result = _fetch_ids_with_retry(chunk=["Test"])

            self.assertEqual(result, [])
            mock_post.assert_called_once_with(names=["Test"])

    def test_returns_empty_when_post_universe_ids_response_has_no_model_dump(self):
        """
        Test that the function returns an empty list when the post_universe_ids response does not have a model_dump method.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "post_universe_ids",
            return_value=SimpleNamespace(),
        ) as mock_post:
            result = _fetch_ids_with_retry(chunk=["TestName"])

            self.assertEqual(result, [])
            mock_post.assert_called_once_with(names=["TestName"])

    def test_returns_empty_when_model_dump_returns_no_characters_key(self):
        """
        Test that the function returns an empty list when the model_dump method of the post_universe_ids response does not return a 'characters' key.

        :return:
        :rtype:
        """

        with patch.object(
            ESIHandler,
            "post_universe_ids",
            return_value=SimpleNamespace(model_dump=lambda: {"not_characters": []}),
        ) as mock_post:
            result = _fetch_ids_with_retry(chunk=["TestName"])

            self.assertEqual(result, [])
            mock_post.assert_called_once_with(names=["TestName"])


class TestCreateCharacters(BaseTestCase):
    """
    Test the create_characters function.
    """

    @patch("aa_intel_tool.helper.eve_character._create_corporation")
    @patch("aa_intel_tool.helper.eve_character._create_alliance")
    @patch("aa_intel_tool.helper.eve_character.EveCharacter")
    @patch("aa_intel_tool.helper.eve_character.ESIHandler.get_alliances_alliance_id")
    @patch(
        "aa_intel_tool.helper.eve_character.ESIHandler.get_corporations_corporation_id"
    )
    @patch("aa_intel_tool.helper.eve_character.ESIHandler.get_universe_factions")
    @patch("aa_intel_tool.helper.eve_character._fetch_affiliations_with_retry")
    def test_creates_characters_with_affiliations(
        self,
        mock_fetch_affiliations,
        mock_get_factions,
        mock_get_corp,
        mock_get_alliance,
        mock_eve_character_class,
        mock_create_alliance,
        mock_create_corporation,
    ):
        """
        Test that characters are created with affiliations when with_affiliation is True, and that related corporations and alliances are created as needed.

        :param mock_fetch_affiliations:
        :type mock_fetch_affiliations:
        :param mock_get_factions:
        :type mock_get_factions:
        :param mock_get_corp:
        :type mock_get_corp:
        :param mock_get_alliance:
        :type mock_get_alliance:
        :param mock_eve_character_class:
        :type mock_eve_character_class:
        :param mock_create_alliance:
        :type mock_create_alliance:
        :param mock_create_corporation:
        :type mock_create_corporation:
        :return:
        :rtype:
        """

        # Input as mappings (dict) so create_characters can index into them
        character_data = [{"id": 12345, "name": "TestCharacter"}]

        # ESI affiliation response uses attribute access
        mock_fetch_affiliations.return_value = [
            SimpleNamespace(
                character_id=12345,
                corporation_id=54321,
                alliance_id=None,
                faction_id=None,
            )
        ]

        # No factions returned
        mock_get_factions.return_value = []

        # Ensure corporation/alliance lookups do not hit network and return objects with attributes used by create_characters
        mock_get_corp.return_value = SimpleNamespace(name="FetchedCorp", ticker="FC")
        mock_get_alliance.return_value = None

        # Mock EveCharacter.objects.bulk_create and .filter behavior
        mock_objects = MagicMock()
        mock_eve_character_class.objects = mock_objects
        expected_qs = MagicMock()
        mock_objects.filter.return_value = expected_qs

        result = create_characters(character_data, with_affiliation=True)

        # bulk_create should have been called with created EveCharacter instances
        mock_objects.bulk_create.assert_called()
        # The function should return the queryset from EveCharacter.objects.filter
        self.assertIs(result, expected_qs)

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
        Test that when with_affiliation is False, the function creates characters without attempting to fetch affiliations or create related corporations/alliances.

        :return:
        :rtype:
        """

        character_data = [
            {"id": 1, "name": "Character One"},
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

        expected_qs = MagicMock()
        expected_qs.count.return_value = 0

        with (
            patch(
                "aa_intel_tool.helper.eve_character._fetch_affiliations_with_retry",
                return_value=affiliations,
            ),
            patch(
                "aa_intel_tool.helper.eve_character.EveCharacter.objects.bulk_create"
            ) as mock_bulk_create,
            patch(
                "aa_intel_tool.helper.eve_character.EveCharacter.objects.filter",
                return_value=expected_qs,
            ),
            patch.object(
                ESIHandler,
                "get_corporations_corporation_id",
                return_value=SimpleNamespace(name="FetchedCorp", ticker="FC"),
            ),
            patch.object(
                ESIHandler,
                "get_alliances_alliance_id",
                return_value=SimpleNamespace(name="FetchedAlliance", ticker="FA"),
            ),
            patch(
                "aa_intel_tool.helper.eve_character._create_alliance"
            ) as mock_create_alliance,
            patch(
                "aa_intel_tool.helper.eve_character._create_corporation"
            ) as mock_create_corporation,
            patch.object(ESIHandler, "get_universe_factions", return_value=[]),
        ):
            result = create_characters(character_data, with_affiliation=False)

            # Ensure we attempted to bulk create characters but did not create affiliations
            mock_bulk_create.assert_called_once()
            mock_create_alliance.assert_not_called()
            mock_create_corporation.assert_not_called()
            self.assertEqual(result.count(), 0)

    def test_creates_alliances_when_alliance_ids_are_present(self):
        """
        Test that when alliance IDs are present in the affiliations, the function calls _create_alliance with the correct set of alliance IDs.

        :return:
        :rtype:
        """

        character_data = [{"id": 1, "name": "Alice"}]
        affiliation = SimpleNamespace(
            character_id=1, corporation_id=None, alliance_id=999, faction_id=None
        )

        with (
            patch(
                "aa_intel_tool.helper.eve_character._fetch_affiliations_with_retry",
                return_value=[affiliation],
            ),
            patch(
                "aa_intel_tool.helper.eve_character.ESIHandler.get_universe_factions",
                return_value=[],
            ),
            patch(
                "aa_intel_tool.helper.eve_character._get_corporation_info_from_affiliation",
                return_value=None,
            ),
            patch(
                "aa_intel_tool.helper.eve_character._get_alliance_info_from_affiliation",
                return_value=None,
            ),
            patch(
                "aa_intel_tool.helper.eve_character.EveCharacter.objects.bulk_create"
            ),
            patch(
                "aa_intel_tool.helper.eve_character.EveCharacter.objects.filter",
                return_value=[],
            ),
            patch(
                "aa_intel_tool.helper.eve_character._create_alliance"
            ) as mock_create_alliance,
        ):
            create_characters(
                character_data_from_esi=character_data, with_affiliation=True
            )
            mock_create_alliance.assert_called_once_with({999})

    def test_does_not_call_create_alliance_when_no_alliance_ids(self):
        """
        Test that when no alliance IDs are present in the affiliations, the function does not call _create_alliance.

        :return:
        :rtype:
        """

        character_data = [{"id": 2, "name": "Bob"}]
        affiliation = SimpleNamespace(
            character_id=2, corporation_id=123, alliance_id=None, faction_id=None
        )

        with (
            patch(
                "aa_intel_tool.helper.eve_character._fetch_affiliations_with_retry",
                return_value=[affiliation],
            ),
            patch(
                "aa_intel_tool.helper.eve_character.ESIHandler.get_universe_factions",
                return_value=[],
            ),
            patch(
                "aa_intel_tool.helper.eve_character._get_corporation_info_from_affiliation",
                return_value=None,
            ),
            patch(
                "aa_intel_tool.helper.eve_character._get_alliance_info_from_affiliation",
                return_value=None,
            ),
            patch(
                "aa_intel_tool.helper.eve_character.EveCharacter.objects.bulk_create"
            ),
            patch(
                "aa_intel_tool.helper.eve_character.EveCharacter.objects.filter",
                return_value=[],
            ),
            patch(
                "aa_intel_tool.helper.eve_character._create_alliance"
            ) as mock_create_alliance,
            patch(
                "aa_intel_tool.helper.eve_character._create_corporation"
            ) as mock_create_corporation,
        ):
            create_characters(
                character_data_from_esi=character_data, with_affiliation=True
            )
            mock_create_alliance.assert_not_called()
            mock_create_corporation.assert_called_once_with({123})


class TestFetchCharacterIdsFromEsi(BaseTestCase):
    """
    Test the fetch_character_ids_from_esi function.
    """

    def test_fetches_character_ids_in_chunks(self):
        """
        Test that character IDs are fetched in chunks when the number of character names exceeds the chunk size, and that results are combined correctly.

        :return:
        :rtype:
        """

        characters_to_fetch = {f"Character {i}" for i in range(1200)}
        per_call = [f"ID {i}" for i in range(400)]

        # return a list (iterable) rather than a SimpleNamespace
        with patch(
            "aa_intel_tool.helper.eve_character._fetch_ids_with_retry",
            return_value=per_call,
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
        Test that if one chunk of character names fails to fetch IDs (e.g., due to an exception),
        the function handles it gracefully and continues fetching IDs for the remaining chunks,
        returning combined results.

        :return:
        :rtype:
        """

        characters_to_fetch = {"Character 1", "Character 2"}
        # return lists (iterables) in side_effect
        with patch(
            "aa_intel_tool.helper.eve_character._fetch_ids_with_retry",
            side_effect=[["ID 1"], []],
        ) as mock_fetch_ids_with_retry:
            result = fetch_character_ids_from_esi(characters_to_fetch)

            self.assertEqual(result, ["ID 1"])
            self.assertEqual(mock_fetch_ids_with_retry.call_count, 1)

    def test_handles_large_chunks_correctly(self):
        """
        Test that when the number of character names is exactly a multiple of the chunk size, all chunks are processed correctly and results are combined.

        :return:
        :rtype:
        """

        characters_to_fetch = {f"Character {i}" for i in range(500)}
        ids = [f"ID {i}" for i in range(500)]
        # return a list (iterable) rather than a SimpleNamespace
        with patch(
            "aa_intel_tool.helper.eve_character._fetch_ids_with_retry",
            return_value=ids,
        ) as mock_fetch_ids_with_retry:
            result = fetch_character_ids_from_esi(characters_to_fetch)

            self.assertEqual(len(result), 500)
            self.assertEqual(result, ids)
            mock_fetch_ids_with_retry.assert_called_once()

    def test_returns_ids_and_logs_debug_when_response_present(self):
        """
        Test that when a response with character IDs is received from ESI, the function returns the IDs and logs a debug message indicating successful processing of the chunk.

        :return:
        :rtype:
        """

        per_call = [{"id": 1, "name": "Alpha"}]
        characters_to_fetch = ["Alpha"]

        with (
            patch(
                "aa_intel_tool.helper.eve_character._fetch_ids_with_retry",
                return_value=per_call,
            ),
            patch("aa_intel_tool.helper.eve_character.logger.debug") as mock_debug,
        ):
            result = fetch_character_ids_from_esi(characters_to_fetch)

            self.assertEqual(result, per_call)
            mock_debug.assert_any_call(
                f"ID information for chunk {1} successfully processed: {per_call}"
            )

    def test_warns_when_no_response_for_chunk(self):
        """
        Test that when no ID information is received from ESI for a chunk of character names, the function logs a warning message indicating the issue.

        :return:
        :rtype:
        """

        characters_to_fetch = ["TestName"]

        with (
            patch(
                "aa_intel_tool.helper.eve_character._fetch_ids_with_retry",
                return_value=[],
            ),
            patch("aa_intel_tool.helper.eve_character.logger.warning") as mock_warning,
        ):
            result = fetch_character_ids_from_esi(characters_to_fetch)

            self.assertEqual(result, [])
            mock_warning.assert_called_once_with(
                f"No ID information received from ESI for chunk {1} with character IDs: {characters_to_fetch}"
            )
