"""
App constants
"""

# Standard Library
import re

# Django
from django.utils.text import slugify

# AA Intel Tool
from aa_intel_tool import __version__

# All internal URLs need to start with this prefix
INTERNAL_URL_PREFIX = "-"

REGEX_PATTERN = {
    "fleetcomp": re.compile(
        r"(?im)^([a-zA-Z0-9 -_]{3,37})[\t](.*)[\t](.*)[\t](.*)[\t](.*)[\t]([0-5] - [0-5] - [0-5])([\t](.*))?$"  # pylint: disable=line-too-long
    ),
    "dscan": re.compile(r"(?im)^(\d+)[\t](.*)[\t](.*)[\t](-|(.*) (km|m|AU)) ?$"),
    "chatlist": re.compile(r"(?im)^[a-zA-Z0-9\u0080-\uFFFF -_]{3,37}$"),
}

SUPPORTED_INTEL_TYPES = [
    {
        "name": "Fleet Composition",
        "parser": "fleetcomp",
        "pattern": REGEX_PATTERN["fleetcomp"],
    },
    {
        "name": "D-Scan",
        "parser": "dscan",
        "pattern": REGEX_PATTERN["dscan"],
    },
    {
        "name": "Chat List",
        "parser": "chatlist",
        "pattern": REGEX_PATTERN["chatlist"],
    },
]


VERBOSE_NAME = "AA Intel Tool"

verbose_name_slugified: str = slugify(VERBOSE_NAME, allow_unicode=True)
github_url: str = "https://github.com/ppfeufer/aa-intel-tool"

USER_AGENT = f"{verbose_name_slugified} v{__version__} {github_url}"
