"""
Fleet composition parser
"""

# pylint: disable=unreachable

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
from aa_intel_tool.app_settings import AppSettings
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.models import Scan
from aa_intel_tool.parser.helper.db import safe_scan_to_db
from aa_intel_tool.parser.module.chatlist import parse as parse_pilots

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def parse(scan_data: list) -> Scan:
    """
    Parse fleet composition

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    message = _("The fleet composition module is currently disabled.")

    if AppSettings.INTELTOOL_ENABLE_MODULE_FLEETCOMP is True:
        pilots = {"list": [], "flying": []}
        lines = []

        # Let's split this list up
        #
        # entry[0] => Pilot Name
        # entry[1] => System
        # entry[2] => Ship Class
        # entry[3] => Ship Type
        # entry[4] => Position in Fleet
        # entry[5] => Skills (FC - WC - SC)
        # entry[6] => Wing Name / Squad Name
        for entry in scan_data:
            line = re.split(pattern=r"\t+", string=entry.rstrip("\t"))

            if len(line) == 6:
                line.append("")

            pilots["list"].append(line[0])
            pilots["flying"].append([line[0], line[2], line[1]])
            lines.append(line)

        for line in lines:
            logger.debug(line[0] + " » " + line[6])

        participation = parse_pilots(
            scan_data=pilots["list"], safe_to_db=False, ignore_limit=True
        )

        parsed_data = {}
        parsed_data.update(participation)

        return safe_scan_to_db(scan_type=Scan.Type.FLEETCOMP, parsed_data=parsed_data)

    raise ParserError(message=message)
