"""
App settings
"""

# Standard Library
from enum import IntEnum
from re import RegexFlag

# Django
from django.conf import settings

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.app_settings import clean_setting
from app_utils.logging import LoggerAddTag

# AA Intel Tool
from aa_intel_tool import __title__

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


class AppSettings:
    """
    App settings from local.py
    """

    # Enable or disable the chat scan module
    # Disabled by default
    INTELTOOL_ENABLE_MODULE_CHATSCAN = clean_setting(
        name="INTELTOOL_ENABLE_MODULE_CHATSCAN", default_value=False, required_type=bool
    )

    # Enable or disable the d-scan module
    # Enabled by default
    INTELTOOL_ENABLE_MODULE_DSCAN = clean_setting(
        name="INTELTOOL_ENABLE_MODULE_DSCAN", default_value=True, required_type=bool
    )

    # Enable or disable the fleet composition module
    # Enabled by default
    INTELTOOL_ENABLE_MODULE_FLEETCOMP = clean_setting(
        name="INTELTOOL_ENABLE_MODULE_FLEETCOMP",
        default_value=True,
        required_type=bool,
    )

    # Scan retention time
    # Sets the time in days for how long the scans will be kept in the database.
    # Set to 0 to keep scans indefinitely.
    INTELTOOL_SCAN_RETENTION_TIME = clean_setting(
        name="INTELTOOL_SCAN_RETENTION_TIME", default_value=30, required_type=int
    )

    # Set the maximum number of pilots allowed per chat scan
    # Set to 0 for no limit.
    INTELTOOL_CHATSCAN_MAX_PILOTS = clean_setting(
        name="INTELTOOL_CHATSCAN_MAX_PILOTS", default_value=500, required_type=int
    )

    # Set the grid size for D-Scans.
    # This defines the size of the grid in which ships and
    # structure are considered to be "on grid"
    INTELTOOL_DSCAN_GRID_SIZE = clean_setting(
        name="INTELTOOL_DSCAN_GRID_SIZE", default_value=10000, required_type=int
    )


class AdditionalEveCategoryId(IntEnum):
    """
    Eve category IDs which are not covered by Eve Universe
    Unfortunately Python doesn't allow to extend eveuniverse.constants.EveCategoryId
    """

    DEPLOYABLE = 22
    STARBASE = 23
    SCANNER_PROBE = 479


class UpwellStructureId(IntEnum):
    """
    Upwell Structure IDs
    """

    ANSIBLEX_JUMP_GATE = 35841


def debug_enabled() -> RegexFlag:
    """
    Check if DEBUG is enabled

    :return:
    :rtype:
    """

    return settings.DEBUG
