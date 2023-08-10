"""
App settings
"""

# Alliance Auth (External Libs)
from app_utils.app_settings import clean_setting


class AppSettings:  # pylint: disable=too-few-public-methods
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
        name="INTELTOOL_ENABLE_MODULE_FLEETCOMP", default_value=True, required_type=bool
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
