"""
App constants
"""

# Standard Library
import re
from enum import IntEnum

# Django
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# AA Intel Tool
import aa_intel_tool.parser.module.chatlist
import aa_intel_tool.parser.module.dscan
import aa_intel_tool.parser.module.fleetcomp
from aa_intel_tool import __version__

# All internal URLs need to start with this prefix
INTERNAL_URL_PREFIX = "-"


# Localised units
distance_units_on_grid: str = """
    km|m    # Client in: English, German, Chinese, French, Japanese, Korean, Spanish
    |км|м   # Russian
"""
distance_units_off_grid: str = """
    AU|     # Client in: English, Chinese, Japanese, Korean, Spanish
    UA|     # Client in: French
    AE|     # German
    а.е.    # Russian
"""

distance_units = f"{distance_units_on_grid}|{distance_units_off_grid}"


class AdditionalEveCategoryId(IntEnum):
    """
    Eve category IDs which are not covered by Eve Universe
    Unfortunately Python doesn't allow to extend eveuniverse.constants.EveCategoryId
    """

    DEPLOYABLE = 22
    STARBASE = 23
    SCANNER_PROBE = 479


# Pre-compiled regex patterns used throughout the app
REGEX_PATTERN = {
    "chatlist": re.compile(pattern=r"(?im)^[a-zA-Z0-9\u0080-\uFFFF -_]{3,37}$"),
    "dscan": re.compile(
        pattern=rf"(?im)^(\d+)[\t](.*)[\t](.*)[\t](-|(.*) ({distance_units}))$",
        flags=re.VERBOSE,
    ),
    "fleetcomp": re.compile(
        pattern=r"(?im)^([a-zA-Z0-9 -_]{3,37})[\t](.*)[\t](.*)[\t](.*)[\t](.*)[\t]([0-5] - [0-5] - [0-5])([\t](.*))?$"  # pylint: disable=line-too-long
    ),
    "localised_on_grid": re.compile(
        pattern=rf"{distance_units_on_grid}", flags=re.VERBOSE
    ),
    "localised_off_grid": re.compile(
        pattern=rf"{distance_units_off_grid}", flags=re.VERBOSE
    ),
}


# Supported intel types and their parameters
SUPPORTED_INTEL_TYPES = {
    "chatlist": {
        "name": _("Chat list"),
        "parser": aa_intel_tool.parser.module.chatlist.parse,
        "pattern": REGEX_PATTERN["chatlist"],
        "template": "aa_intel_tool/views/scan/chatlist.html",
    },
    "dscan": {
        "name": _("D-Scan"),
        "parser": aa_intel_tool.parser.module.dscan.parse,
        "pattern": REGEX_PATTERN["dscan"],
        "template": "aa_intel_tool/views/scan/dscan.html",
    },
    "fleetcomp": {
        "name": _("Fleet composition"),
        "parser": aa_intel_tool.parser.module.fleetcomp.parse,
        "pattern": REGEX_PATTERN["fleetcomp"],
        "template": "aa_intel_tool/views/scan/fleetcomp.html",
    },
}


# Building our user agent for ESI calls
VERBOSE_NAME = "AA Intel Tool"
verbose_name_slugified: str = slugify(VERBOSE_NAME, allow_unicode=True)
github_url: str = "https://github.com/ppfeufer/aa-intel-tool"
USER_AGENT = f"{verbose_name_slugified} v{__version__} {github_url}"
