"""
App constants
"""

# Standard Library
import re

# Django
from django.utils.text import slugify

# AA Intel Tool
# import aa_intel_tool.parser.module.chatlist
import aa_intel_tool.parser.module.dscan
import aa_intel_tool.parser.module.fleetcomp
from aa_intel_tool import __version__

# All internal URLs need to start with this prefix
INTERNAL_URL_PREFIX = "-"

REGEX_PATTERN = {
    # "chatlist": re.compile(r"(?im)^[a-zA-Z0-9\u0080-\uFFFF -_]{3,37}$"),
    "dscan": re.compile(r"(?im)^(\d+)[\t](.*)[\t](.*)[\t](-|(.*) (km|m|AU))$"),
    "fleetcomp": re.compile(
        r"(?im)^([a-zA-Z0-9 -_]{3,37})[\t](.*)[\t](.*)[\t](.*)[\t](.*)[\t]([0-5] - [0-5] - [0-5])([\t](.*))?$"  # pylint: disable=line-too-long
    ),
}

SUPPORTED_INTEL_TYPES = {
    # "chatlist": {
    #     "name": "Chat List",
    #     "parser": aa_intel_tool.parser.module.chatlist.parse,
    #     "pattern": REGEX_PATTERN["chatlist"],
    # },
    "dscan": {
        "name": "D-Scan",
        "parser": aa_intel_tool.parser.module.dscan.parse,
        "pattern": REGEX_PATTERN["dscan"],
    },
    "fleetcomp": {
        "name": "Fleet Composition",
        "parser": aa_intel_tool.parser.module.fleetcomp.parse,
        "pattern": REGEX_PATTERN["fleetcomp"],
    },
}


VERBOSE_NAME = "AA Intel Tool"

verbose_name_slugified: str = slugify(VERBOSE_NAME, allow_unicode=True)
github_url: str = "https://github.com/ppfeufer/aa-intel-tool"

USER_AGENT = f"{verbose_name_slugified} v{__version__} {github_url}"
