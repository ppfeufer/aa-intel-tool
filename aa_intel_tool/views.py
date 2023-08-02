"""
The views …
"""

# Django
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# AA Intel Tool
from aa_intel_tool.form import IntelForm


def index(request: WSGIRequest) -> HttpResponse:
    """
    Intel tool index (basically just the form)

    :return:
    :rtype:
    """

    form = IntelForm()

    context = {"form": form}

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

    context = {
        "scan_hash": scan_hash,
    }

    return render(
        request=request, template_name="aa_intel_tool/views/scan.html", context=context
    )
