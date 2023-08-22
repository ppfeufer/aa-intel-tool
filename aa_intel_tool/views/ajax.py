"""
Ajax views
"""

# Django
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

# AA Intel Tool
from aa_intel_tool.models import ScanData


def get_scan_data(
    request: WSGIRequest,  # pylint: disable=unused-argument
    scan_hash: str,
    scan_section: ScanData.Section,
) -> JsonResponse:
    """
    Get scan data for a specific section

    :param request:
    :type request:
    :param scan_hash:
    :type scan_hash:
    :param scan_section:
    :type scan_section:
    :return:
    :rtype:
    """

    try:
        scan_data = ScanData.objects.filter(  # pylint: disable=no-member
            scan_id__exact=scan_hash, section__exact=scan_section
        ).get()
        processed_data = scan_data.processed_data
    except ScanData.DoesNotExist:  # pylint: disable=no-member
        processed_data = {}

    return JsonResponse(data=processed_data, safe=False)
