"""
Test for the providers module.
"""

# Standard Library
import logging
from unittest.mock import MagicMock, patch

# Third Party
from aiopenapi3 import ContentTypeError, RequestError

# Alliance Auth
from esi.exceptions import HTTPClientError, HTTPNotModified

# AA Intel Tool
from aa_intel_tool import __title__, providers
from aa_intel_tool.providers.applogger import AppLogger
from aa_intel_tool.providers.esi import ESIHandler
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
        app_logger = AppLogger(logger)

        with self.assertLogs("test_logger", level="INFO") as log:
            app_logger.info("This is a test message")

        self.assertIn(f"[{__title__}] This is a test message", log.output[0])

    def test_handles_empty_message(self):
        """
        Tests that the AppLogger handles an empty log message correctly.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger)

        with self.assertLogs("test_logger", level="INFO") as log:
            app_logger.info("")

        self.assertIn(f"[{__title__}] ", log.output[0])


class TestESIHandlerResult(BaseTestCase):
    """
    Test the ESIHandler.result method.
    """

    def test_returns_result_when_operation_succeeds(self):
        """
        Test returning an ESIHandler result.

        :return:
        :rtype:
        """

        operation = MagicMock()
        operation.operation = MagicMock(operationId="GetSomething")
        operation.result.return_value = {"data": 1}

        result = ESIHandler.result(
            operation=operation,
            use_etag=True,
            return_response=False,
            force_refresh=False,
            use_cache=True,
        )

        self.assertEqual(result, {"data": 1})
        operation.result.assert_called_once_with(
            use_etag=True, return_response=False, force_refresh=False, use_cache=True
        )

    def test_returns_result_and_response_when_return_response_true(self):
        """
        Test returning an ESIHandler result along with the response when `return_response` is set to `True`.

        :return:
        :rtype:
        """

        operation = MagicMock()
        operation.operation = MagicMock(operationId="GetSomething")
        response_obj = MagicMock()
        operation.result.return_value = ([1, 2, 3], response_obj)

        result = ESIHandler.result(
            operation=operation,
            use_etag=False,
            return_response=True,
            force_refresh=True,
            use_cache=False,
        )

        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], [1, 2, 3])
        self.assertIs(result[1], response_obj)
        operation.result.assert_called_once_with(
            use_etag=False, return_response=True, force_refresh=True, use_cache=False
        )

    def test_returns_none_on_http_not_modified(self):
        """
        Test returns `None` on HTTP Not Modified.

        :return:
        :rtype:
        """

        operation = MagicMock()
        operation.operation = MagicMock(operationId="GetSomething")
        # HTTPNotModified requires status_code and headers
        operation.result.side_effect = HTTPNotModified(304, {})

        result = ESIHandler.result(operation=operation, return_response=False)

        self.assertIsNone(result)

    def test_returns_none_tuple_on_http_not_modified_when_return_response_true(self):
        """
        Test returns `None` on HTTP Not Modified when `return_response` is set to `True`.

        :return:
        :rtype:
        """

        operation = MagicMock()
        operation.operation = MagicMock(operationId="GetSomething")
        # HTTPNotModified requires status_code and headers
        operation.result.side_effect = HTTPNotModified(304, {})

        result = ESIHandler.result(operation=operation, return_response=True)

        self.assertEqual(result, (None, None))

    def test_returns_none_on_content_type_error(self):
        """
        Test returns `None` on content type error.

        :return:
        :rtype:
        """

        operation = MagicMock()
        operation.operation = MagicMock(operationId="GetSomething")
        # ContentTypeError requires operation, content_type, message and response
        operation.result.side_effect = ContentTypeError(
            None, "application/json", "invalid", None
        )

        result = ESIHandler.result(operation=operation)

        self.assertIsNone(result)

    def test_returns_none_on_client_or_request_error(self):
        """
        Test returns `None` on client or request error.

        :return:
        :rtype:
        """

        # HTTPClientError requires status_code, headers and data; construct with dummy values
        client_exc = HTTPClientError(500, {}, None)
        # RequestError requires operation, request, data and parameters
        request_exc = RequestError(None, None, None, None)

        for exc in (client_exc, request_exc):
            operation = MagicMock()
            operation.operation = MagicMock(operationId="GetSomething")
            operation.result.side_effect = exc

            result = ESIHandler.result(operation=operation)
            self.assertIsNone(result)

    def test_passes_extra_kwargs_to_operation_result(self):
        """
        Test passes extra kwargs to operation result.

        :return:
        :rtype:
        """

        operation = MagicMock()
        operation.operation = MagicMock(operationId="GetSomething")
        operation.result.return_value = "ok"

        result = ESIHandler.result(
            operation=operation,
            use_etag=False,
            return_response=False,
            force_refresh=True,
            use_cache=False,
            foo="bar",
        )

        self.assertEqual(result, "ok")
        operation.result.assert_called_once_with(
            use_etag=False,
            return_response=False,
            force_refresh=True,
            use_cache=False,
            foo="bar",
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
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
            patch.object(providers.esi, "esi", new=MagicMock()),
        ):
            result = ESIHandler.post_universe_ids(names=["Nonexistent Name"])

            self.assertIsNone(result)
            mock_result.assert_called_once()
