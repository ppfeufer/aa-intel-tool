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

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.app_settings import AppSettings
from aa_intel_tool.constants import SUPPORTED_INTEL_TYPES
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.form import IntelForm
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.general import parse_intel

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def index(request: WSGIRequest) -> HttpResponse:
    """
    Intel tool index (basically just the form)

    :return:
    :rtype:
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
                errormessage = _("The provided data could not be parsed.") + f" ({exc})"
                messages.error(request=request, message=errormessage)

            # Catching every other exception we can't think of (hopefully)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                exception_caught = True
                errormessage = (
                    _("(System Error) Something unexpected happened.") + f" ({exc})"
                )
                messages.error(request=request, message=errormessage)

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

    :param request:
    :type request:
    :param scan_hash:
    :type scan_hash:
    :return:
    :rtype:
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
        "parser_title": SUPPORTED_INTEL_TYPES[intel_scan.scan_type]["name"],
        "app_settings": AppSettings,
    }

    if intel_scan.scan_type in SUPPORTED_INTEL_TYPES:
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
