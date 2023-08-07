"""
The views …
"""

# Django
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

# AA Intel Tool
from aa_intel_tool.app_settings import AppSettings
from aa_intel_tool.form import IntelForm
from aa_intel_tool.models import Scan
from aa_intel_tool.parser.general import parse_intel


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
            scan_data = form.cleaned_data["eve_intel"]

            max_allowed_pilots = AppSettings.INTELTOOL_CHATSCAN_MAX_PILOTS
            if 0 < max_allowed_pilots < len(scan_data.split()):
                messages.error(
                    request=request,
                    message=ngettext(
                        singular=f"Chat scans are currently limited to a maximum of {max_allowed_pilots} pilot per scan. Your list of pilots exceeds this limit.",  # pylint: disable=line-too-long
                        plural=f"Chat scans are currently limited to a maximum of {max_allowed_pilots} pilots per scan. Your list of pilots exceeds this limit.",  # pylint: disable=line-too-long
                        number=max_allowed_pilots,
                    ),
                )

                return redirect(to="aa_intel_tool:intel_tool_index")

            parsed_intel = parse_intel(form_data=scan_data)

            if parsed_intel is None:
                messages.error(
                    request=request,
                    message=_(
                        "The provided data could not be parsed. "
                        "Please check and try again."
                    ),
                )

                return redirect(to="aa_intel_tool:intel_tool_index")

            return redirect(to="aa_intel_tool:intel_tool_scan", scan_hash=parsed_intel)

        context = {"form": form, "app_settings": AppSettings}

    # If a GET (or any other method) we'll create a blank form
    else:
        form = IntelForm()

        context = {"form": form, "app_settings": AppSettings}

    return render(
        request=request, template_name="aa_intel_tool/views/index.html", context=context
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

    scan_data = {
        "scan_type": intel_scan.scan_type,
        "created": intel_scan.created,
        "raw_data": intel_scan.raw_data,
        # "processed_data": intel_scan.processed_data,
    }

    context = {
        "scan_hash": scan_hash,
        "scan": scan_data,
    }

    if intel_scan.scan_type == "chatlist":
        return render(
            request=request,
            template_name="aa_intel_tool/views/scan/chatlist.html",
            context=context,
        )

    messages.error(
        request=request,
        message=_("The scan you were looking for could not be found."),
    )

    return redirect(to="aa_intel_tool:intel_tool_index")
