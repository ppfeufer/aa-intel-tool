"""
App settings
"""

# Alliance Auth (External Libs)
from app_utils.app_settings import clean_setting


class AppSettings:  # pylint: disable=too-few-public-methods
    """
    App settings from local.py
    """

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
