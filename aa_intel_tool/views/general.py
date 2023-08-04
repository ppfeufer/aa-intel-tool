"""
The views …
"""
# Standard Library
import json

# Django
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

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

            parsed_intel = parse_intel(form_data=scan_data)

            if parsed_intel is None:
                messages.error(
                    request=request,
                    message=_("The submitted data could not be parsed."),
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
        intel_scan = None

    context = {
        "scan_hash": scan_hash,
        "scan_type": intel_scan.scan_type if intel_scan is not None else None,
        "raw_data": intel_scan.raw_data if intel_scan is not None else None,
        "processed_data": json.loads(intel_scan.processed_data)
        if intel_scan is not None
        else None,
        "app_settings": AppSettings,
    }

    return render(
        request=request, template_name="aa_intel_tool/views/scan.html", context=context
    )
