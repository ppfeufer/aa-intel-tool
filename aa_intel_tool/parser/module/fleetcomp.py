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

# from aa_intel_tool.models import Scan
# from aa_intel_tool.parser.helper.db import safe_scan_to_db
from aa_intel_tool.parser.module.chatlist import parse as parse_pilots

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def parse(scan_data: list) -> tuple:
    """
    Parse chat list

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    message = _("The fleet composition module is currently disabled.")

    if AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN is True:
        return None, _("The fleet composition module is not yet finished, be patient …")

        logger.debug(msg=scan_data)

        # Let's split this list up
        #
        # [0] => Pilot Name
        # [1] => System
        # [2] => Ship Class
        # [3] => Ship Type
        # [4] => Position in Fleet
        # [5] => Skills (FC - WC - SC)
        # [6] => Wing Name / Squad Name
        pilots = {"list": [], "flying": []}
        lines = []
        for entry in scan_data:
            line = re.split(pattern=r"\t+", string=entry.rstrip("\t"))

            if len(line) == 6:
                line.append("")

            pilots["list"].append(line[0])
            pilots["flying"].append([line[0], line[2], line[1]])
            lines.append(line)

        for line in lines:
            logger.debug(line[0] + " » " + line[6])

        logger.debug(msg=pilots)

        pilotlist = parse_pilots(scan_data=pilots["list"], safe_to_db=False)

        logger.debug(msg=pilotlist)

        # parsed_data = {
        #     "general_information": None,
        #     "ship_classes": None,
        #     "ship_types": None,
        #     "composition": None,
        #     "pilots": pilotlist["pilots"] if pilotlist is not None else None,
        #     "corporations": pilotlist["corporations"],
        #     "alliances": pilotlist["alliances"],
        # }

        return None

        # return safe_scan_to_db(scan_type=Scan.Type.CHATLIST, parsed_data=parsed_data)

    return None, message
