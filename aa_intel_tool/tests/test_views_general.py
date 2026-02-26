"""
Tests for the general views of the AA Intel Tool application.
"""

# Standard Library
from http import HTTPStatus
from unittest.mock import MagicMock, Mock, patch

# Django
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.shortcuts import redirect
from django.test import RequestFactory

# AA Intel Tool
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.models import Scan
from aa_intel_tool.tests import BaseTestCase
from aa_intel_tool.views import general as general_view
from aa_intel_tool.views.general import scan


class TestViewIndex(BaseTestCase):
    """
    Tests for the index view
    """

    def test_redirects_to_scan_view_on_valid_form_submission_direct_call(self):
        """
        Testing redirection to scan view on valid form submission

        :return:
        :rtype:
        """

        form_data = {"eve_intel": "valid intel data"}
        rf = RequestFactory()
        request = rf.post("/intel/", data=form_data)

        with (
            patch("aa_intel_tool.views.general.IntelForm") as mock_form,
            patch("aa_intel_tool.views.general.parse_intel") as mock_parse,
        ):
            mock_form.return_value.is_valid.return_value = True
            mock_form.return_value.cleaned_data = form_data
            mock_parse.return_value = "valid_scan_hash"

            response = general_view.index(request)

            self.assertEqual(response.status_code, HTTPStatus.FOUND)
            self.assertEqual(response["Location"], "/intel/scan/valid_scan_hash/")

    def test_shows_error_message_on_parser_error_direct_call(self):
        """
        Testing error message on parser error during form submission

        :return:
        :rtype:
        """

        form_data = {"eve_intel": "invalid intel data"}
        rf = RequestFactory()
        request = rf.post("/intel/", data=form_data)

        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

        with (
            patch("aa_intel_tool.views.general.IntelForm") as mock_form,
            patch("aa_intel_tool.views.general.parse_intel") as mock_parse,
        ):
            mock_form.return_value.is_valid.return_value = True
            mock_form.return_value.cleaned_data = form_data
            mock_parse.side_effect = ParserError("Parsing failed")

            response = general_view.index(request)

            self.assertEqual(response.status_code, HTTPStatus.FOUND)

            messages = [str(m) for m in get_messages(request)]

            # ensure the general parse-failure message is present
            self.assertTrue(
                any("The provided data could not be parsed." in m for m in messages),
                f"messages were: {messages}",
            )
            # ensure the exception detail is included somewhere
            self.assertTrue(
                any("Parsing failed" in m for m in messages),
                f"messages were: {messages}",
            )

    def test_shows_error_message_on_unexpected_exception_direct_call(self):
        """
        Testing error message on unexpected exception during form submission

        :return:
        :rtype:
        """

        form_data = {"eve_intel": "unexpected error data"}
        rf = RequestFactory()
        request = rf.post("/intel/", data=form_data)

        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

        with (
            patch("aa_intel_tool.views.general.IntelForm") as mock_form,
            patch("aa_intel_tool.views.general.parse_intel") as mock_parse,
        ):
            mock_form.return_value.is_valid.return_value = True
            mock_form.return_value.cleaned_data = form_data
            mock_parse.side_effect = Exception("Unexpected error")

            response = general_view.index(request)

            self.assertEqual(response.status_code, HTTPStatus.FOUND)

            messages = [str(m) for m in get_messages(request)]

            self.assertTrue(
                any(
                    "Something unexpected happened" in m or "(System Error)" in m
                    for m in messages
                ),
                f"messages were: {messages}",
            )
            self.assertTrue(
                any("Unexpected error" in m for m in messages),
                f"messages were: {messages}",
            )

    def test_renders_blank_form_on_get_request_direct_call(self):
        """
        Testing rendering of blank form on GET request

        :return:
        :rtype:
        """

        rf = RequestFactory()
        request = rf.get("/intel/")

        response = general_view.index(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("<form", response.content.decode("utf-8"))


class TestViewScan(BaseTestCase):
    """
    Tests for the scan view
    """

    def test_redirects_to_index_for_unsupported_scan_type(self):
        """
        Testing redirection to index view for unsupported scan type

        :return:
        :rtype:
        """

        scan_instance = MagicMock(scan_type="unsupported_type")

        with (
            patch("aa_intel_tool.models.Scan.objects.exclude") as mock_exclude,
            patch("aa_intel_tool.views.general.SUPPORTED_INTEL_TYPES", {}),
        ):
            mock_exclude.return_value.get.return_value = scan_instance
            request = MagicMock()

            response = scan(request, "valid_hash")

            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                response.url, redirect("aa_intel_tool:intel_tool_index").url
            )

    def test_shows_error_message_when_scan_does_not_exist(self):
        """
        Testing error message when scan does not exist

        :return:
        :rtype:
        """

        rf = RequestFactory()
        request = rf.get("/intel/scan/nonexistent-scan-hash/")

        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        request._messages = FallbackStorage(request)

        with patch("aa_intel_tool.views.general.Scan.objects.exclude") as mock_exclude:
            mock_exclude.return_value.get.side_effect = Scan.DoesNotExist

            response = general_view.scan(request, scan_hash="nonexistent-scan-hash")

            self.assertEqual(response.status_code, HTTPStatus.FOUND)

            messages = [str(m) for m in get_messages(request)]

            self.assertTrue(
                any(
                    "The scan you were looking for could not be found." in m
                    for m in messages
                ),
                f"messages were: {messages}",
            )

    def test_renders_correct_template_for_supported_scan_type(self):
        """
        Testing rendering of correct template for supported scan type

        :return:
        :rtype:
        """

        rf = RequestFactory()
        request = rf.get("/intel/scan/supported-scan-hash/")

        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

        with patch("aa_intel_tool.views.general.Scan.objects.exclude") as mock_exclude:
            mock_scan = Mock()
            mock_scan.scan_type = "supported_type"
            mock_scan.created = "2023-01-01"
            mock_scan.raw_data = "raw intel data"
            mock_exclude.return_value.get.return_value = mock_scan

            # dummy response that mimics a rendered template response
            dummy_response = Mock()
            dummy_response.status_code = HTTPStatus.OK
            dummy_response.templates = [
                type("T", (), {"name": "supported_template.html"})()
            ]

            with (
                patch(
                    "aa_intel_tool.views.general.SUPPORTED_INTEL_TYPES",
                    {
                        "supported_type": {
                            "name": "Supported Type",
                            "template": "supported_template.html",
                        }
                    },
                ),
                patch(
                    "aa_intel_tool.views.general.render", return_value=dummy_response
                ) as mock_render,
            ):
                response = general_view.scan(request, scan_hash="supported-scan-hash")

                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, "supported_template.html")
                mock_render.assert_called_once()
