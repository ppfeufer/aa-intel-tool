"""
Intel Parser
"""

# Standard Library
import re
from typing import Optional


def check_intel_type(scan_data: str) -> Optional[str]:
    """
    Check which intel type we have

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    intel_type = None

    # Supported Intel types
    # Regex Pattern => Type Key
    supported_types = {
        r"/^([a-zA-Z0-9 -_]{3,37})[\t](.*)[\t](.* \/ .*) ?$/": "fleetcomp",
        r"/^\d+[\t](.*)[\t](-|\d(.*)) ?$/m": "dscan",
        r"/^[a-zA-Z0-9 -_]{3,37}$/m": "chatlist",
    }

    for key, value in supported_types.items():
        if re.match(pattern=key, string=scan_data):
            intel_type = value

    return intel_type


def parse_dscan(scan_data: str):
    """
    Parse D-Scan

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    return ""


def parse_fleetcomp(scan_data: str):
    """
    Parse fleet composition

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    return ""


def parse_chatlist(scan_data: str):
    """
    Parse chat list

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    return ""


def parse_intel(scan_data: str):
    """
    Parse intel

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    intel_type = check_intel_type(scan_data=scan_data)

    switch = {
        "dscan": parse_dscan,
        "chatlist": parse_chatlist,
        "fleetcomp": parse_fleetcomp,
    }

    if intel_type in switch:
        return switch[intel_type]()
