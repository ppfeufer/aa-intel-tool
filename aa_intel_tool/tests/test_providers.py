"""
Test for the providers module.
"""

# Standard Library
import logging
from http import HTTPStatus
from unittest.mock import MagicMock, patch

# Third Party
from aiopenapi3 import ContentTypeError

# Alliance Auth
from esi.exceptions import HTTPClientError, HTTPNotModified

# AA Intel Tool
from aa_intel_tool import providers
from aa_intel_tool.providers import AppLogger, ESIHandler
from aa_intel_tool.tests import BaseTestCase


class TestAppLogger(BaseTestCase):
    """
    Test the AppLogger provider.
    """

    def test_adds_prefix_to_log_message(self):
        """
        Tests that the AppLogger correctly adds a prefix to log messages.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger, "PREFIX")

        with self.assertLogs("test_logger", level="INFO") as log:
            app_logger.info("This is a test message")

        self.assertIn("[PREFIX] This is a test message", log.output[0])

    def test_handles_empty_prefix(self):
        """
        Tests that the AppLogger handles an empty prefix correctly.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger, "")

        with self.assertLogs("test_logger", level="INFO") as log:
            app_logger.info("Message without prefix")

        self.assertIn("Message without prefix", log.output[0])

    def test_handles_non_string_prefix(self):
        """
        Tests that the AppLogger handles a non-string prefix correctly.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger, 123)

        with self.assertLogs("test_logger", level="INFO") as log:
            app_logger.info("Message with numeric prefix")

        self.assertIn("[123] Message with numeric prefix", log.output[0])

    def test_handles_special_characters_in_prefix(self):
        """
        Tests that the AppLogger handles special characters in the prefix correctly.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger, "!@#$%^&*()")

        with self.assertLogs("test_logger", level="INFO") as log:
            app_logger.info("Message with special characters in prefix")

        self.assertIn(
            "[!@#$%^&*()] Message with special characters in prefix", log.output[0]
        )

    def test_handles_empty_message(self):
        """
        Tests that the AppLogger handles an empty log message correctly.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger, "PREFIX")

        with self.assertLogs("test_logger", level="INFO") as log:
            app_logger.info("")

        self.assertIn("[PREFIX] ", log.output[0])


class TestESIHandlerResult(BaseTestCase):
    """
    Test the ESIHandler.result method.
    """

    def test_handles_successful_operation(self):
        """
        Test that a successful ESI operation returns the expected result.

        :return:
        :rtype:
        """

        mock_operation = MagicMock()
        mock_operation.result.return_value = "success"

        response = ESIHandler.result(mock_operation)

        self.assertEqual(response, "success")
        mock_operation.result.assert_called_once()

    def test_handles_http_not_modified_exception(self):
        """
        Test that an HTTPNotModified exception is handled correctly.

        :return:
        :rtype:
        """

        mock_operation = MagicMock()
        mock_operation.result.side_effect = HTTPNotModified(
            status_code=HTTPStatus.NOT_MODIFIED, headers={}
        )

        response = ESIHandler.result(mock_operation)

        self.assertIsNone(response)
        mock_operation.result.assert_called_once()

    def test_handles_content_type_error(self):
        """
        Test that a ContentTypeError exception is handled correctly.

        :return:
        :rtype:
        """

        mock_operation = MagicMock()
        mock_response = MagicMock()
        mock_operation.result.side_effect = ContentTypeError(
            operation=mock_operation,
            content_type="application/json",
            message="Invalid content type",
            response=mock_response,
        )

        response = ESIHandler.result(mock_operation)

        self.assertIsNone(response)
        mock_operation.result.assert_called_once()

    def test_returns_none_when_http_client_error_occurs(self):
        """
        Test that an HTTPClientError exception is raised correctly.

        :return:
        :rtype:
        """

        mock_operation = MagicMock()
        mock_operation.result.side_effect = HTTPClientError(
            HTTPStatus.BAD_REQUEST, headers={}, data={}
        )

        response = ESIHandler.result(mock_operation)

        self.assertIsNone(response)
        mock_operation.result.assert_called_once()

    def test_passes_extra_parameters_to_operation(self):
        """
        Test that extra parameters are passed correctly to the ESI operation.

        :return:
        :rtype:
        """

        mock_operation = MagicMock()
        mock_operation.result.return_value = "success"

        response = ESIHandler.result(
            mock_operation, use_etag=False, extra_param="value"
        )

        self.assertEqual(response, "success")
        mock_operation.result.assert_called_once_with(
            use_etag=False,
            return_response=False,
            force_refresh=False,
            use_cache=True,
            extra_param="value",
        )


class TestESIHandlerGetAlliancesAllianceId(BaseTestCase):
    """
    Test the ESIHandler.get_alliances_alliance_id method.
    """

    def test_retrieves_alliance_information_when_valid_id_provided(self):
        """
        Test that the method retrieves alliance information when a valid alliance ID is provided.

        :return:
        :rtype:
        """

        with (
            patch.object(
                ESIHandler,
                "result",
                return_value={"alliance_id": 12345, "name": "Test Alliance"},
            ) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_alliances_alliance_id(alliance_id=12345)

            self.assertEqual(result, {"alliance_id": 12345, "name": "Test Alliance"})
            mock_result.assert_called_once()

    def test_returns_none_when_alliance_id_not_found(self):
        """
        Test that the method returns None when the alliance ID is not found.

        :return:
        :rtype:
        """

        with (
            patch.object(ESIHandler, "result", return_value=None) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_alliances_alliance_id(alliance_id=99999)

            self.assertIsNone(result)
            mock_result.assert_called_once()

    def test_handles_etag_caching_correctly(self):
        """
        Test that the method handles ETag caching correctly when use_etag is True.

        :return:
        :rtype:
        """

        with (
            patch.object(
                ESIHandler,
                "result",
                return_value={"alliance_id": 12345, "name": "Cached Alliance"},
            ) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_alliances_alliance_id(
                alliance_id=12345, use_etag=True
            )

            self.assertEqual(result, {"alliance_id": 12345, "name": "Cached Alliance"})
            mock_result.assert_called_once()

    def test_returns_none_when_esi_returns_not_modified(self):
        """
        Test that the method returns None when the ESI operation raises an HTTPNotModified exception.

        :return:
        :rtype:
        """

        with (
            patch.object(ESIHandler, "result", return_value=None) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_alliances_alliance_id(alliance_id=12345)

            self.assertIsNone(result)
            mock_result.assert_called_once()

    def test_returns_none_when_content_type_error_occurs(self):
        """
        Test that the method returns None when the ESI operation raises a ContentTypeError exception.

        :return:
        :rtype:
        """

        with (
            patch.object(ESIHandler, "result", return_value=None) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_alliances_alliance_id(alliance_id=12345)

            self.assertIsNone(result)
            mock_result.assert_called_once()


class TestESIHandlerGetCorporationsCorporationId(BaseTestCase):
    """
    Test the ESIHandler.get_corporations_corporation_id method.
    """

    def test_retrieves_corporation_information_when_valid_id_provided(self):
        """
        Test that the method retrieves corporation information when a valid corporation ID is provided.

        :return:
        :rtype:
        """

        with (
            patch.object(
                ESIHandler,
                "result",
                return_value={"corporation_id": 67890, "name": "Test Corporation"},
            ) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_corporations_corporation_id(corporation_id=67890)

            self.assertEqual(
                result, {"corporation_id": 67890, "name": "Test Corporation"}
            )
            mock_result.assert_called_once()

    def test_returns_none_when_corporation_id_not_found(self):
        """
        Test that the method returns None when the corporation ID is not found.

        :return:
        :rtype:
        """

        with (
            patch.object(ESIHandler, "result", return_value=None) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_corporations_corporation_id(corporation_id=99999)

            self.assertIsNone(result)
            mock_result.assert_called_once()

    def test_handles_etag_caching_correctly_for_corporation(self):
        """
        Test that the method handles ETag caching correctly for corporation information when use_etag is True.

        :return:
        :rtype:
        """

        with (
            patch.object(
                ESIHandler,
                "result",
                return_value={"corporation_id": 67890, "name": "Cached Corporation"},
            ) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_corporations_corporation_id(
                corporation_id=67890, use_etag=True
            )

            self.assertEqual(
                result, {"corporation_id": 67890, "name": "Cached Corporation"}
            )
            mock_result.assert_called_once()

    def test_returns_none_when_esi_returns_not_modified_for_corporation(self):
        """
        Test that the method returns None when the ESI operation raises an HTTPNotModified exception for corporation information.

        :return:
        :rtype:
        """

        with (
            patch.object(ESIHandler, "result", return_value=None) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_corporations_corporation_id(corporation_id=67890)

            self.assertIsNone(result)
            mock_result.assert_called_once()


class TestGetUniverseFactions(BaseTestCase):
    """
    Test the ESIHandler.get_universe_factions method.
    """

    def test_retrieves_factions_successfully(self):
        """
        Test that the method retrieves factions successfully when the ESI operation returns valid data.

        :return:
        :rtype:
        """

        with (
            patch.object(
                ESIHandler,
                "result",
                return_value=[{"faction_id": 1, "name": "Faction One"}],
            ) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_universe_factions()

            self.assertEqual(result, [{"faction_id": 1, "name": "Faction One"}])
            mock_result.assert_called_once()

    def test_returns_none_when_factions_not_found(self):
        """
        Test that the method returns None when the ESI operation returns None, indicating that factions were not found.

        :return:
        :rtype:
        """

        with (
            patch.object(ESIHandler, "result", return_value=None) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_universe_factions()

            self.assertIsNone(result)
            mock_result.assert_called_once()

    def test_handles_etag_caching_correctly_for_factions(self):
        """
        Test that the method handles ETag caching correctly for factions when use_etag is True.

        :return:
        :rtype:
        """

        with (
            patch.object(
                ESIHandler,
                "result",
                return_value=[{"faction_id": 1, "name": "Cached Faction"}],
            ) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.get_universe_factions(use_etag=True)

            self.assertEqual(result, [{"faction_id": 1, "name": "Cached Faction"}])
            mock_result.assert_called_once()


class TestPostCharactersAffiliation(BaseTestCase):
    """
    Test the ESIHandler.post_characters_affiliation method.
    """

    def test_retrieves_affiliations_successfully(self):
        """
        Test that the method retrieves affiliations successfully when the ESI operation returns valid data.

        :return:
        :rtype:
        """

        with (
            patch.object(
                ESIHandler, "result", return_value=[{"id": 1, "name": "Character One"}]
            ) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.post_characters_affiliation(ids=[1, 2, 3])

            self.assertEqual(result, [{"id": 1, "name": "Character One"}])
            mock_result.assert_called_once()

    def test_returns_none_when_affiliations_not_found(self):
        """
        Test that the method returns None when the ESI operation returns None, indicating that affiliations were not found.

        :return:
        :rtype:
        """

        with (
            patch.object(ESIHandler, "result", return_value=None) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.post_characters_affiliation(ids=[99999])

            self.assertIsNone(result)
            mock_result.assert_called_once()

    def test_handles_empty_ids_list_correctly(self):
        """
        Test that the method handles an empty list of IDs correctly, which should return an empty list.

        :return:
        :rtype:
        """

        with (
            patch.object(ESIHandler, "result", return_value=[]) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.post_characters_affiliation(ids=[])

            self.assertEqual(result, [])
            mock_result.assert_called_once()


class TestPostUniverseIds(BaseTestCase):
    """
    Test the ESIHandler.post_universe_ids method.
    """

    def test_retrieves_ids_for_valid_names(self):
        """
        Test that the method retrieves IDs successfully when valid names are provided and the ESI operation returns valid data.

        :return:
        :rtype:
        """

        with (
            patch.object(
                ESIHandler, "result", return_value=[{"id": 1, "name": "Valid Name"}]
            ) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.post_universe_ids(names=["Valid Name"])

            self.assertEqual(result, [{"id": 1, "name": "Valid Name"}])
            mock_result.assert_called_once()

    def test_returns_none_when_names_not_found(self):
        """
        Test that the method returns None when the ESI operation returns None, indicating that no IDs were found for the provided names.

        :return:
        :rtype:
        """

        with (
            patch.object(ESIHandler, "result", return_value=None) as mock_result,
            patch.object(providers, "esi", new=MagicMock()),
        ):
            result = ESIHandler.post_universe_ids(names=["Nonexistent Name"])

            self.assertIsNone(result)
            mock_result.assert_called_once()
