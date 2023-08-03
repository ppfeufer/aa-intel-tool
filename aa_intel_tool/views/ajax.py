"""
The views …
"""

# Django
from django.core.handlers.wsgi import WSGIRequest

# AA Intel Tool
from aa_intel_tool.form import IntelForm


def parse_form_data(request: WSGIRequest):
    """
    Parse form data

    :param request:
    :type request:
    :return:
    :rtype:
    """

    if request.method == "POST":
        # Create a form instance and populate it with data from the request
        form = IntelForm(data=request.POST)

        # Check whether it's valid:
        if form.is_valid():
            scan_data = form.cleaned_data["eve_intel"]

            return scan_data

    return None
