"""
the views ....
"""

# Django
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# AA Intel Tool
from aa_intel_tool.form import IntelForm
from aa_intel_tool.utils import get_template_view


def index(request: WSGIRequest) -> HttpResponse:
    """
    intel tool index
    basically just the form
    :return:
    :rtype:
    """

    form = IntelForm()

    context = {"template_view": get_template_view(request), "form": form}

    return render(request, "aa_intel_tool/view/index.html", context)


def scan(request: WSGIRequest, scan_hash: str):
    context = {
        "template_view": get_template_view(request),
    }

    return render(request, "aa_intel_tool/view/scan.html", context)
