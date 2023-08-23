"""
DB helper for our parser
"""

# AA Intel Tool
from aa_intel_tool.models import Scan, ScanData


def safe_scan_to_db(scan_type: Scan.Type, parsed_data: dict) -> Scan:
    """
    Saving scan data to the DB

    :param scan_type:
    :type scan_type:
    :param parsed_data:
    :type parsed_data:
    :return:
    :rtype:
    """

    # Creating a new Scan object
    new_scan = Scan(scan_type=scan_type)
    new_scan.save()

    # Creating the associated ScanData objects
    for scan_data in parsed_data.values():
        ScanData(
            scan=new_scan,
            section=scan_data["section"],
            processed_data=scan_data["data"],
        ).save()

    # Return the Scan object
    return new_scan
