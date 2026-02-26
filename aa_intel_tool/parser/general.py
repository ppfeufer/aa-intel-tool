"""
General parser functions
"""

# Standard Library
import re

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.constants import SUPPORTED_INTEL_TYPES
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def check_intel_type(scan_data: list) -> str:
    """
    Check which intel type we have

    :param scan_data: List of strings to check for intel type patterns
    :type scan_data: list
    :return: Intel type as a string
    :rtype: str
    """

    logger.info(msg="Checking intel type …")
    logger.info(msg=f"Supported intel types: {list(SUPPORTED_INTEL_TYPES.keys())}")

    for intel_type, intel_type_attributes in SUPPORTED_INTEL_TYPES.items():
        logger.info(msg=f"Checking for intel type: {intel_type_attributes['name']}")
        logger.info(msg=f"Using pattern: {intel_type_attributes['pattern']}")

        if all(
            re.match(pattern=intel_type_attributes["pattern"], string=string)
            for string in scan_data
        ):
            logger.info(msg=f"Detected intel type: {intel_type_attributes['name']}")

            return intel_type

    raise ParserError(
        message=str(
            _(
                "No suitable parser found. Input is not a supported intel type or malformed …"
            )
        )
    )


def parse_intel(form_data: str) -> str:
    """
    Parse intel

    :param form_data: Raw intel data as a string
    :type form_data: str
    :return: Hash of the created Scan object
    :rtype: str
    """
    scan_data = form_data.splitlines()

    if not scan_data:
        raise ParserError(message=str(_("No data to parse …")))

    try:
        intel_type = check_intel_type(scan_data=scan_data)
        new_scan = SUPPORTED_INTEL_TYPES[intel_type]["parser"](scan_data=scan_data)
    except ParserError as exc:
        # Re-raise the Exception
        raise ParserError(message=exc.message) from exc

    new_scan.raw_data = form_data
    new_scan.save()

    return new_scan.hash
