"""
D-Scan parser
"""

# Django
from django.utils.translation import gettext_lazy as _

# AA Intel Tool
from aa_intel_tool.app_settings import AppSettings


def parse(scan_data: list) -> tuple:  # pylint: disable=unused-argument
    """
    Parse D-Scan

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    message = _("The D-Scan module is currently disabled.")

    if AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN is True:
        return None, _("The D-Scan module is not yet finished, be patient …")

    return None, message
