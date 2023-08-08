"""
D-Scan parser
"""

# AA Intel Tool
from aa_intel_tool.app_settings import AppSettings


def parse(scan_data: list):  # pylint: disable=unused-argument
    """
    Parse D-Scan

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    if AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN is False:
        return None

    return "D-Scan"
