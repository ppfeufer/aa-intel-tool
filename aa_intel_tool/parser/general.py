"""
General parser functions
"""

# Standard Library
import re
from typing import Optional

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.constants import SUPPORTED_INTEL_TYPES
from aa_intel_tool.parser.module import chatlist, dscan, fleetcomp

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def check_intel_type(scan_data: list) -> Optional[str]:
    """
    Check which intel type we have

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    for intel_type in SUPPORTED_INTEL_TYPES:
        if all(
            re.match(pattern=intel_type["pattern"], string=string)
            for string in scan_data
        ):
            return intel_type["parser"]

    return None


def parse_intel(form_data: str) -> tuple:
    """
    Parse intel

    :param form_data:
    :type form_data:
    :return:
    :rtype:
    """

    scan_data = form_data.splitlines()

    if len(scan_data) > 0:
        intel_type = check_intel_type(scan_data=scan_data)

        switch = {
            "dscan": dscan.parse,
            "chatlist": chatlist.parse,
            "fleetcomp": fleetcomp.parse,
        }

        if intel_type in switch:
            new_scan, message = switch[intel_type](scan_data=scan_data)

            if new_scan is not None:
                new_scan.raw_data = form_data
                new_scan.save()

                return new_scan.hash, message

            return None, message

    return None, _("No data to parse …")
