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
    # INTELTOOL_ENABLE_MODULE_CHATSCAN = clean_setting(
    #     name="INTELTOOL_ENABLE_MODULE_CHATSCAN", default_value=False, required_type=bool
    # )

    # Hard disabling this module for now, since CCP can't handle ESI requests and is
    # banning IPs that are doing "too many" ESI requests, what ever "too many" means.
    # But since we don't want our users getting banned just for using this app, this
    # module is currently deactivated and we discourage everyone from activating it in
    # the code. Sorry for this, blame CCP's incompetency …
    INTELTOOL_ENABLE_MODULE_CHATSCAN = False

    # Enable or disable the d-scan module
    # Enabled by default
    INTELTOOL_ENABLE_MODULE_DSCAN = clean_setting(
        name="INTELTOOL_ENABLE_MODULE_DSCAN", default_value=True, required_type=bool
    )

    # Enable or disable the fleet composition module
    # Enabled by default
    INTELTOOL_ENABLE_MODULE_FLEETCOMP = clean_setting(
        name="INTELTOOL_ENABLE_MODULE_FLEETCOMP",
        default_value=False,
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
