"""
The views …
"""

# Django
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.app_settings import AppSettings
from aa_intel_tool.constants import SUPPORTED_INTEL_TYPES
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.form import IntelForm
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.general import parse_intel
from aa_intel_tool.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view

    :param request: The HTTP request object containing metadata about the request and user input
    :type request: WSGIRequest
    :return: An HTTP response object that renders the index page with the appropriate context, including the form for submitting intel data and application settings
    :rtype: HttpResponse
    """

    if request.method == "POST":
        # Create a form instance and populate it with data from the request
        form = IntelForm(data=request.POST)

        # Check whether it's valid:
        if form.is_valid():
            exception_caught = False
            scan_data = form.cleaned_data["eve_intel"]

            try:
                parsed_intel = parse_intel(form_data=scan_data)

            # Catching our own parser exceptions
            except ParserError as exc:
                exception_caught = True

                messages.error(
                    request=request,
                    message=_("The provided data could not be parsed. ({exc})").format(
                        exc=exc
                    ),
                )

            # Catching every other exception we can't think of (hopefully)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                exception_caught = True

                messages.error(
                    request=request,
                    message=_(
                        "(System Error) Something unexpected happened. ({exc})"
                    ).format(exc=exc),
                )

            if exception_caught:
                return redirect(to="aa_intel_tool:intel_tool_index")

            return redirect(to="aa_intel_tool:intel_tool_scan", scan_hash=parsed_intel)

        context = {"form": form, "app_settings": AppSettings}

    # If a GET (or any other method) we'll create a blank form
    else:
        form = IntelForm()
        context = {"form": form, "app_settings": AppSettings}

    return render(
        request=request,
        template_name="aa_intel_tool/views/index.html",
        context=context,
    )


def scan(request: WSGIRequest, scan_hash: str):
    """
    Scan view

    :param request: The HTTP request object containing metadata about the request and user input
    :type request: WSGIRequest
    :param scan_hash: The unique identifier for the scan to be displayed, typically a hash value that corresponds to a specific Scan object in the database
    :type scan_hash: str
    :return: An HTTP response object that renders the scan page with the appropriate context, including the scan data and application settings, or redirects to the index page with an error message if the scan is not found
    :rtype: HttpResponse
    """

    try:
        # pylint: disable=no-member
        intel_scan = Scan.objects.exclude(scan_type=Scan.Type.INVALID).get(pk=scan_hash)
    except Scan.DoesNotExist:
        messages.error(
            request=request,
            message=_("The scan you were looking for could not be found."),
        )

        return redirect(to="aa_intel_tool:intel_tool_index")

    logger.debug(msg=f"Intel Type: {intel_scan.scan_type}")

    scan_data = {
        "scan_type": intel_scan.scan_type,
        "created": intel_scan.created,
        "raw_data": intel_scan.raw_data,
    }

    context = {
        "scan_hash": scan_hash,
        "scan": scan_data,
        "scan_data_section": ScanData.Section,
        "app_settings": AppSettings,
    }

    if intel_scan.scan_type in SUPPORTED_INTEL_TYPES:
        context["parser_title"] = SUPPORTED_INTEL_TYPES[intel_scan.scan_type]["name"]

        return render(
            request=request,
            template_name=SUPPORTED_INTEL_TYPES[intel_scan.scan_type]["template"],
            context=context,
        )

    messages.error(
        request=request,
        message=_("The scan you were looking for could not be found."),
    )

    return redirect(to="aa_intel_tool:intel_tool_index")
