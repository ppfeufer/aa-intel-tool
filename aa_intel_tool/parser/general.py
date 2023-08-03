"""
General parser functions
"""

# Standard Library
import re
from typing import Optional

# AA Intel Tool
from aa_intel_tool import parser
from aa_intel_tool.constants import SUPPORTED_INTEL_TYPES


def check_intel_type(scan_data: list) -> Optional[str]:
    """
    Check which intel type we have

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    # Supported Intel types
    # Regex Pattern => Type Key
    # supported_types = {
    #     r"(?im)^([a-zA-Z0-9 -_]{3,37})[\t](.*)[\t](.* \/ .*) ?$": "fleetcomp",
    #     r"(?im)^\d+[\t](.*)[\t](-|\d(.*)) ?$": "dscan",
    #     r"(?im)^[a-zA-Z0-9 -_]{3,37}$": "chatlist",
    # }
    #
    # for pattern, intel_type in supported_types.items():
    #     if all(re.match(pattern=pattern, string=string) for string in scan_data):
    #         return intel_type

    for intel_type in SUPPORTED_INTEL_TYPES:
        if all(
            re.match(pattern=intel_type["pattern"], string=string)
            for string in scan_data
        ):
            return intel_type["parser"]

    return None


def parse_intel(form_data: str):
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
            "dscan": parser.dscan.parse,
            "chatlist": parser.chatlist.parse,
            "fleetcomp": parser.fleetcomp.parse,
        }

        if intel_type in switch:
            return switch[intel_type]()

    return None
