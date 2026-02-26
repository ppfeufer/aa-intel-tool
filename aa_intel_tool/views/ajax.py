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

    :param request: The HTTP request object (not used in this function but included for consistency with Django view patterns)
    :type request: WSGIRequest
    :param scan_hash: The unique identifier for the scan whose data is being requested
    :type scan_hash: str
    :param scan_section: The specific section of the scan data being requested, defined as a member of the ScanData.Section enumeration
    :type scan_section: ScanData.Section
    :return: A JsonResponse containing the processed data for the specified scan and section, or an empty dictionary if no data is found
    :rtype: JsonResponse
    """

    try:
        scan_data = ScanData.objects.filter(  # pylint: disable=no-member
            scan_id__exact=scan_hash, section__exact=scan_section
        ).get()
        processed_data = scan_data.processed_data
    except ScanData.DoesNotExist:  # pylint: disable=no-member
        processed_data = {}

    return JsonResponse(data=processed_data, safe=False)
