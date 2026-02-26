"""
App settings
"""

# Standard Library
from enum import IntEnum
from re import RegexFlag
from typing import Any

# Django
from django.conf import settings

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def _clean_setting(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    name: str,
    default_value: Any,
    min_value: int | None = None,
    max_value: int | None = None,
    required_type: type | None = None,
    choices: list | None = None,
) -> Any:
    """
    Clean a setting from Django settings.

    Will use default_value if setting is not defined.
    Will use minimum or maximum value if respective boundary is exceeded.

    :param name:
    :type name:
    :param default_value:
    :type default_value:
    :param min_value:
    :type min_value:
    :param max_value:
    :type max_value:
    :param required_type:
    :type required_type:
    :param choices:
    :type choices:
    :return:
    :rtype:
    """

    if default_value is None and not required_type:
        raise ValueError("You must specify a required_type for None defaults")

    required_type_2 = type(default_value) if required_type is None else required_type

    if not isinstance(required_type_2, type):
        raise TypeError("required_type must be a type when defined")

    if min_value is None and issubclass(required_type_2, int):
        min_value = 0

    if issubclass(required_type_2, int) and default_value is not None:
        if min_value is not None and default_value < min_value:
            raise ValueError("default_value can not be below min_value")

        if max_value is not None and default_value > max_value:
            raise ValueError("default_value can not be above max_value")

    if not hasattr(settings, name):
        cleaned_value = default_value
    else:
        dirty_value = getattr(settings, name)

        if dirty_value is None or (
            isinstance(dirty_value, required_type_2)
            and all(
                (
                    min_value is None or dirty_value >= min_value,
                    max_value is None or dirty_value <= max_value,
                    choices is None or dirty_value in choices,
                )
            )
        ):
            cleaned_value = dirty_value
        elif (
            isinstance(dirty_value, required_type_2)
            and min_value is not None
            and dirty_value < min_value
        ):
            logger.warning(
                "Your setting for %s it not valid. Please correct it. "
                "Using minimum value for now: %s",
                name,
                min_value,
            )
            cleaned_value = min_value
        elif (
            isinstance(dirty_value, required_type_2)
            and max_value is not None
            and dirty_value > max_value
        ):
            logger.warning(
                "Your setting for %s it not valid. Please correct it. "
                "Using maximum value for now: %s",
                name,
                max_value,
            )
            cleaned_value = max_value
        else:
            logger.warning(
                "Your setting for %s it not valid. Please correct it. "
                "Using default for now: %s",
                name,
                default_value,
            )
            cleaned_value = default_value

    return cleaned_value


class AppSettings:
    """
    App settings from local.py
    """

    # Enable or disable the chat scan module
    # Disabled by default
    INTELTOOL_ENABLE_MODULE_CHATSCAN = _clean_setting(
        name="INTELTOOL_ENABLE_MODULE_CHATSCAN", default_value=False, required_type=bool
    )

    # Enable or disable the d-scan module
    # Enabled by default
    INTELTOOL_ENABLE_MODULE_DSCAN = _clean_setting(
        name="INTELTOOL_ENABLE_MODULE_DSCAN", default_value=True, required_type=bool
    )

    # Enable or disable the fleet composition module
    # Enabled by default
    INTELTOOL_ENABLE_MODULE_FLEETCOMP = _clean_setting(
        name="INTELTOOL_ENABLE_MODULE_FLEETCOMP",
        default_value=True,
        required_type=bool,
    )

    # Scan retention time
    # Sets the time in days for how long the scans will be kept in the database.
    # Set to 0 to keep scans indefinitely.
    INTELTOOL_SCAN_RETENTION_TIME = _clean_setting(
        name="INTELTOOL_SCAN_RETENTION_TIME", default_value=30, required_type=int
    )

    # Set the maximum number of pilots allowed per chat scan
    # Set to 0 for no limit.
    INTELTOOL_CHATSCAN_MAX_PILOTS = _clean_setting(
        name="INTELTOOL_CHATSCAN_MAX_PILOTS", default_value=500, required_type=int
    )

    # Set the grid size for D-Scans.
    # This defines the size of the grid in which ships and
    # structure are considered to be "on grid"
    INTELTOOL_DSCAN_GRID_SIZE = _clean_setting(
        name="INTELTOOL_DSCAN_GRID_SIZE", default_value=10000, required_type=int
    )


class EVECategory(IntEnum):
    """
    EVE Online category IDs
    """

    SHIP = 6
    DEPLOYABLE = 22
    STARBASE = 23
    STRUCTURE = 65


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
