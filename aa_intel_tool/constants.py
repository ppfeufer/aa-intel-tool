"""
App constants
"""
# Standard Library
import re

SUPPORTED_INTEL_TYPES = [
    {
        "name": "Fleet Composition",
        "parser": "fleetcomp",
        "pattern": re.compile(r"(?im)^([a-zA-Z0-9 -_]{3,37})[\t](.*)[\t](.* / .*) ?$"),
    },
    {
        "name": "D-Scan",
        "parser": "dscan",
        "pattern": re.compile(r"(?im)^\d+[\t](.*)[\t](-|\d(.*)) ?$"),
    },
    {
        "name": "Chat List",
        "parser": "chatlist",
        "pattern": re.compile(r"(?im)^[a-zA-Z0-9 -_]{3,37}$"),
    },
]
