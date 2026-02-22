"""
Test for the providers module.
"""

# Standard Library
import logging
from http import HTTPStatus
from unittest.mock import MagicMock

# Third Party
from aiopenapi3 import ContentTypeError

# Alliance Auth
from esi.exceptions import HTTPClientError, HTTPNotModified

# AA Intel Tool
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


class TestESIHandler(BaseTestCase):
    """
    Test the ESIHandler provider.
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
