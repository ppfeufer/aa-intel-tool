"""
App constants
"""

# Standard Library
import os
import re

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from esi import __version__ as esi_version

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
    AU      # Client in: English, Chinese, Japanese, Korean, Spanish
    |UA     # Client in: French
    |AE     # German
    |а.е.   # Russian
"""

distance_units: str = f"{distance_units_on_grid}|{distance_units_off_grid}"


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
APP_NAME = "aa-intel-tool"
PACKAGE_NAME = "aa_intel_tool"
APP_VERBOSE_NAME = "AA Intel Tool"
APP_VERBOSE_NAME_USERAGENT = "AA-Intel-Tool"
GITHUB_URL = f"https://github.com/ppfeufer/{APP_NAME}"
USER_AGENT = f"{APP_VERBOSE_NAME_USERAGENT}/{__version__} (+{GITHUB_URL}) Django-ESI/{esi_version}"

APP_BASE_DIR = os.path.join(os.path.dirname(__file__))
APP_STATIC_DIR = os.path.join(APP_BASE_DIR, "static", PACKAGE_NAME)
