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
    scan_data_objects = []
    for scan_data in parsed_data.values():
        scan_data_objects.append(
            ScanData(
                scan=new_scan,
                section=scan_data["section"],
                processed_data=scan_data["data"],
            )
        )

    # Saving ScanData objects
    ScanData.objects.bulk_create(scan_data_objects)

    # Return the Scan object
    return new_scan
