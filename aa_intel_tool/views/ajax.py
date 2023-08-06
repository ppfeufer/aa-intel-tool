"""
Ajax views
"""

# Django
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

# AA Intel Tool
from aa_intel_tool.models import ScanData


def get_pilot_list(
    request: WSGIRequest,  # pylint: disable=unused-argument
    scan_hash: str,
) -> JsonResponse:
    """
    Get the pilot list for a scan

    :param scan_hash:
    :type scan_hash:
    :return:
    :rtype:
    """

    try:
        pilotlist = (
            ScanData.objects.filter(  # pylint: disable=no-member
                scan_id__exact=scan_hash, section__exact=ScanData.Section.PILOTLIST
            )
            .exclude(section=ScanData.Section.INVALID)
            .get()
        )
        processed_data = pilotlist.processed_data
    except ScanData.DoesNotExist:  # pylint: disable=no-member
        processed_data = None

    return JsonResponse(data=processed_data, safe=False)


def get_corporation_list(
    request: WSGIRequest,  # pylint: disable=unused-argument
    scan_hash: str,
) -> JsonResponse:
    """
    Get the corporation list for a scan

    :param scan_hash:
    :type scan_hash:
    :return:
    :rtype:
    """

    try:
        corporationlist = (
            ScanData.objects.filter(  # pylint: disable=no-member
                scan_id__exact=scan_hash,
                section__exact=ScanData.Section.CORPORATIONLIST,
            )
            .exclude(section=ScanData.Section.INVALID)
            .get()
        )

        processed_data = corporationlist.processed_data
    except ScanData.DoesNotExist:  # pylint: disable=no-member
        processed_data = None

    return JsonResponse(data=processed_data, safe=False)


def get_alliance_list(
    request: WSGIRequest,  # pylint: disable=unused-argument
    scan_hash: str,
) -> JsonResponse:
    """
    Get the alliance list for a scan

    :param scan_hash:
    :type scan_hash:
    :return:
    :rtype:
    """

    try:
        alliancelist = (
            ScanData.objects.filter(  # pylint: disable=no-member
                scan_id__exact=scan_hash, section__exact=ScanData.Section.ALLIANCELIST
            )
            .exclude(section=ScanData.Section.INVALID)
            .get()
        )

        processed_data = alliancelist.processed_data
    except ScanData.DoesNotExist:  # pylint: disable=no-member
        processed_data = None

    return JsonResponse(data=processed_data, safe=False)
