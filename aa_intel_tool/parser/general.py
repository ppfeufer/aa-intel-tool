"""
General parser functions
"""

# Standard Library
import re

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.constants import SUPPORTED_INTEL_TYPES
from aa_intel_tool.exceptions import ParserError

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def check_intel_type(scan_data: list) -> str:
    """
    Check which intel type we have

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    for intel_type, intel_type_attributes in SUPPORTED_INTEL_TYPES.items():
        if all(
            re.match(pattern=intel_type_attributes["pattern"], string=string)
            for string in scan_data
        ):
            logger.debug(msg=f"Detected intel type: {intel_type_attributes['name']}")

            return intel_type

    raise ParserError(
        message=_(
            "No suitable parser found. Input is not a supported intel type or malformed …"
        )
    )


def parse_intel(form_data: str) -> str:
    """
    Parse intel

    :param form_data:
    :type form_data:
    :return:
    :rtype:
    """
    scan_data = form_data.splitlines()

    if not scan_data:
        raise ParserError(message=_("No data to parse …"))

    try:
        intel_type = check_intel_type(scan_data=scan_data)
        new_scan = SUPPORTED_INTEL_TYPES[intel_type]["parser"](scan_data=scan_data)
    except ParserError as exc:
        # Re-raise the Exception
        raise ParserError(message=exc.message) from exc

    new_scan.raw_data = form_data
    new_scan.save()

    return new_scan.hash
