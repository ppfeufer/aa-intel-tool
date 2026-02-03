"""
App constants
"""

# Standard Library
import re
from enum import Enum

# Django
from django.utils.translation import gettext_lazy as _

# AA Intel Tool
import aa_intel_tool.parser.module.chatlist
import aa_intel_tool.parser.module.dscan
import aa_intel_tool.parser.module.fleetcomp

# All internal URLs need to start with this prefix
INTERNAL_URL_PREFIX = "-"


class DistanceUnits(Enum):
    """
    Localised distance units
    """

    ON_GRID = r"""
        km|m    # Client in: English, German, Chinese, French, Japanese, Korean, Spanish
        |км|м   # Client in: Russian
    """
    OFF_GRID = r"""
        AU      # Client in: English, Chinese, Japanese, Korean, Spanish
        |UA     # Client in: French
        |AE     # Client in: German
        |а.е.   # Client in: Russian
    """


DISTANCE_UNITS: str = f"{DistanceUnits.ON_GRID.value}|{DistanceUnits.OFF_GRID.value}"


class RegexPattern(Enum):
    """
    Pre-compiled regex patterns
    """

    CHATLIST = re.compile(pattern=r"(?im)^[a-zA-Z0-9\u0080-\uFFFF -_]{3,37}$")
    DSCAN = re.compile(
        pattern=rf"(?im)^(\d+)[\t](.*)[\t](.*)[\t](-|(.*) ({DISTANCE_UNITS}))$",
        flags=re.VERBOSE,
    )
    FLEETCOMP = re.compile(
        pattern=r"(?im)^([a-zA-Z0-9 -_]{3,37})[\t](.*)[\t](.*)[\t](.*)[\t](.*)[\t]([0-5] - [0-5] - [0-5])([\t](.*))?$"
    )
    LOCALISED_ON_GRID = re.compile(
        pattern=rf"{DistanceUnits.ON_GRID.value}", flags=re.VERBOSE
    )
    LOCALISED_OFF_GRID = re.compile(
        pattern=rf"{DistanceUnits.OFF_GRID.value}", flags=re.VERBOSE
    )


# Supported intel types and their parameters
SUPPORTED_INTEL_TYPES = {
    "chatlist": {
        "name": _("Chat list"),
        "parser": aa_intel_tool.parser.module.chatlist.parse,
        "pattern": RegexPattern.CHATLIST.value,
        "template": "aa_intel_tool/views/scan/chatlist.html",
    },
    "dscan": {
        "name": _("D-Scan"),
        "parser": aa_intel_tool.parser.module.dscan.parse,
        "pattern": RegexPattern.DSCAN.value,
        "template": "aa_intel_tool/views/scan/dscan.html",
    },
    "fleetcomp": {
        "name": _("Fleet composition"),
        "parser": aa_intel_tool.parser.module.fleetcomp.parse,
        "pattern": RegexPattern.FLEETCOMP.value,
        "template": "aa_intel_tool/views/scan/fleetcomp.html",
    },
}
