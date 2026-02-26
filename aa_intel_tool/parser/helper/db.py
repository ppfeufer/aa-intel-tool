"""
DB helper for our parser
"""

# AA Intel Tool
from aa_intel_tool.models import Scan, ScanData


def safe_scan_to_db(scan_type: Scan.Type, parsed_data: dict) -> Scan:
    """
    Saving scan data to the DB

    :param scan_type: The type of the scan being saved
    :type scan_type: Scan.Type
    :param parsed_data: The parsed data to be saved, structured as a dict with section names as keys and dicts with 'section' and 'data' as values
    :type parsed_data: dict
    :return: The created Scan object
    :rtype: Scan
    """

    # Creating a new Scan object and saving it
    new_scan = Scan.objects.create(scan_type=scan_type)

    # Creating and saving the associated ScanData objects
    ScanData.objects.bulk_create(
        [
            ScanData(
                scan=new_scan,
                section=scan_data["section"],
                processed_data=scan_data["data"],
            )
            for scan_data in parsed_data.values()
        ]
    )

    # Return the Scan object
    return new_scan
