"""
App settings
"""

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
    # This defines the size of teh grid in which ships and
    # structure are considered to be "on grid"
    INTELTOOL_DSCAN_GRID_SIZE = clean_setting(
        name="INTELTOOL_DSCAN_GRID_SIZE", default_value=10000, required_type=int
    )

    @classmethod
    def allianceauth_major_version(cls):
        """
        Get the major version of the current installed Alliance Auth instance

        :return:
        :rtype:
        """

        return version.parse(version=allianceauth__version).major

    @classmethod
    def template_path(cls) -> str:
        """
        Get template path

        This is used to determine if we have Alliance Auth v4 or still v3, in which case we
        have to fall back to the legacy templates to ensure backwards compatibility

        :return:
        :rtype:
        """

        current_aa_major = cls.allianceauth_major_version()
        app_name = AaIntelToolConfig.name

        if current_aa_major < 4:
            logger.debug(
                msg="Alliance Auth v3 detected, falling back to legacy templates …"
            )

            return f"{app_name}/legacy_templates"

        return app_name
