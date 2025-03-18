"""
D-Scan parser
"""

# Standard Library
import re
from collections import defaultdict

# Django
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.eveonline.evelinks import eveimageserver
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from eveuniverse.constants import EveCategoryId
from eveuniverse.models import EveType

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.app_settings import (
    AdditionalEveCategoryId,
    AppSettings,
    UpwellStructureId,
)
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.helper.data_structure import dict_to_list
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.helper.db import safe_scan_to_db

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def _is_on_grid(distance: str) -> bool:
    """
    Determine if something is "on grid" or not

    :param distance:
    :type distance:
    :return:
    :rtype:
    """

    # AA Intel Tool
    from aa_intel_tool.constants import (  # pylint: disable=import-outside-toplevel
        REGEX_PATTERN,
    )

    # Check if we have a distance
    match = re.search(pattern=REGEX_PATTERN["localised_on_grid"], string=distance)

    # Check if the distance is within the grid size
    if match:
        distance_sanitised = int(re.sub(pattern=r"[^0-9]", repl="", string=distance))
        return distance_sanitised <= AppSettings.INTELTOOL_DSCAN_GRID_SIZE

    return False


def _get_type_info_dict(eve_type: tuple) -> dict:
    """
    Get the eve_type info dict

    eve_type[0] = ID
    eve_type[1] = Name
    eve_type[2] = Group ID
    eve_type[3] = Group Name

    :param eve_type:
    :type eve_type:
    :return:
    :rtype:
    """

    return {
        "id": eve_type[0],
        "name": eve_type[1],
        "type_id": eve_type[2],
        "type_name": eve_type[3],
        "image": eveimageserver.type_icon_url(type_id=eve_type[0], size=32),
    }


def _get_ships(eve_types: QuerySet, counter: dict) -> dict:
    """
    Get the ships
    This will be the content of the following tables in the D-Scan view:
    » All Ships
    » On Grid
    » Off Grid
    » Ship Types

    :param eve_types:
    :type eve_types:
    :param counter:
    :type counter:
    :return:
    :rtype:
    """

    ships = {"all": {}, "ongrid": {}, "offgrid": {}, "types": {}}

    def _add_ship_info(ship_dict: dict, eve_type: tuple, count: int):
        """
        Add ship info to the ship_dict

        :param ship_dict:
        :type ship_dict:
        :param eve_type:
        :type eve_type:
        :param count:
        :type count:
        :return:
        :rtype:
        """

        if eve_type[1] not in ship_dict:
            ship_dict[eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
            ship_dict[eve_type[1]]["count"] = count
            ship_dict[eve_type[1]]["mass"] = eve_type[4] * count

    # Ship types
    # Get all ship types
    #
    # Ship type list:
    #   - eve_type[0] = ID
    #   - eve_type[1] = Name
    #   - eve_type[2] = Group ID
    #   - eve_type[3] = Group Name
    #   - eve_type[4] = Mass
    eve_types_ships = eve_types.filter(
        eve_group__eve_category_id__exact=EveCategoryId.SHIP
    )

    # Loop through all ships types
    for eve_type in list(eve_types_ships):
        # Info for "All Ships" table
        if eve_type[0] in counter["all"]:
            _add_ship_info(
                ship_dict=ships["all"],
                eve_type=eve_type,
                count=counter["all"][eve_type[0]],
            )

        # Info for "On Grid" table
        if eve_type[0] in counter["ongrid"]:
            _add_ship_info(
                ship_dict=ships["ongrid"],
                eve_type=eve_type,
                count=counter["ongrid"][eve_type[0]],
            )

        # Info for "Off Grid" table
        if eve_type[0] in counter["offgrid"]:
            _add_ship_info(
                ship_dict=ships["offgrid"],
                eve_type=eve_type,
                count=counter["offgrid"][eve_type[0]],
            )

        # Info for "Ship Types" table
        if eve_type[3] not in ships["types"]:
            ships["types"][eve_type[3]] = {
                "id": eve_type[2],
                "name": eve_type[3],
                "count": 0,
            }

        # Add the count to the ship types
        ships["types"][eve_type[3]]["count"] += counter["all"][eve_type[0]]

    return {
        "all": dict_to_list(input_dict=ships["all"]),
        "ongrid": dict_to_list(input_dict=ships["ongrid"]),
        "offgrid": dict_to_list(input_dict=ships["offgrid"]),
        "types": dict_to_list(input_dict=ships["types"]),
    }


def _get_upwell_structures_on_grid(
    eve_types: QuerySet, counter: dict, ansiblex_destination: str = None
) -> list:
    """
    Get all Upwell structures that are on grid

    :param eve_types:
    :type eve_types:
    :param counter:
    :type counter:
    :return:
    :rtype:
    """

    eve_types_structures = eve_types.filter(
        eve_group__eve_category_id__exact=EveCategoryId.STRUCTURE
    )

    upwell_structures = {
        eve_type[1]: {
            **_get_type_info_dict(eve_type=eve_type),
            "count": counter["ongrid"][eve_type[0]],
            "name": (
                f"{eve_type[1]} » {ansiblex_destination}"
                if eve_type[0] == UpwellStructureId.ANSIBLEX_JUMP_GATE
                and ansiblex_destination
                else eve_type[1]
            ),
        }
        for eve_type in list(eve_types_structures)
        if eve_type[0] in counter["ongrid"]
    }

    return dict_to_list(input_dict=upwell_structures)


def _get_deployables_on_grid(eve_types: QuerySet, counter: dict) -> list:
    """
    Get all deployables that are on grid

    :param eve_types:
    :type eve_types:
    :param counter:
    :type counter:
    :return:
    :rtype:
    """

    eve_types_deployables = eve_types.filter(
        eve_group__eve_category_id__exact=AdditionalEveCategoryId.DEPLOYABLE
    )

    deployables = {
        eve_type[1]: {
            **_get_type_info_dict(eve_type=eve_type),
            "count": counter["ongrid"][eve_type[0]],
        }
        for eve_type in list(eve_types_deployables)
        if eve_type[0] in counter["ongrid"]
    }

    return dict_to_list(input_dict=deployables)


def _get_starbases_on_grid(eve_types: QuerySet, counter: dict) -> list:
    """
    Get all starbases and starbase modules that are on grid

    :param eve_types:
    :type eve_types:
    :param counter:
    :type counter:
    :return:
    :rtype:
    """

    eve_types_starbase = eve_types.filter(
        eve_group__eve_category_id__exact=AdditionalEveCategoryId.STARBASE
    )

    starbases = {
        eve_type[1]: {
            **_get_type_info_dict(eve_type=eve_type),
            "count": counter["ongrid"][eve_type[0]],
        }
        for eve_type in list(eve_types_starbase)
        if eve_type[0] in counter["ongrid"]
    }

    return dict_to_list(input_dict=starbases)


def _get_ansiblex_jumpgate_destination(ansiblex_name: str) -> str:
    """
    Get the Ansiblex Jump Gate destination system

    :param ansiblex_name:
    :type ansiblex_name:
    :return:
    :rtype:
    """

    return re.split(
        pattern=r" » ", string=re.split(pattern=r" - ", string=ansiblex_name)[0]
    )[1]


def _get_scan_details(scan_data: list) -> tuple:
    """
    Split the D-Scan data into more convenient parts

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    # AA Intel Tool
    from aa_intel_tool.constants import (  # pylint: disable=import-outside-toplevel
        REGEX_PATTERN,
    )

    ansiblex_destination = None
    counter = defaultdict(lambda: defaultdict(int))
    eve_ids = defaultdict(list)

    # Let's split this list up
    #
    # line.group(1) => Item ID
    # line.group(2) => Name
    # line.group(3) => Ship Class / Structure Type
    # line.group(4) => Distance
    #
    # Loop through all lines
    for entry in scan_data:
        # Apparently you can copy/paste a tab into the ship name, which will cause the split by tab to fail.
        # The regex is detecting the D-Scan correctly though. But splitting by tab might put the ship class as distance.
        # See https://github.com/ppfeufer/aa-intel-tool/issues/82
        #
        # This is why we use re.search() to get the parts of the D-Scan entry, instead of re-split()
        #
        # Thanks CCP for sanitizing your inputs! 😂
        line = re.search(pattern=REGEX_PATTERN["dscan"], string=entry)
        entry_id = int(line.group(1))

        counter["all"][entry_id] += 1

        # Check if the entry is "on grid" or not
        if _is_on_grid(distance=line.group(4)):
            counter["ongrid"][entry_id] += 1

            # If it is an Ansiblex Jump Gate, get its destination system
            if entry_id == UpwellStructureId.ANSIBLEX_JUMP_GATE:
                ansiblex_destination = _get_ansiblex_jumpgate_destination(
                    ansiblex_name=line.group(2)
                )

            eve_ids["ongrid"].append(entry_id)
        else:
            counter["offgrid"][entry_id] += 1
            eve_ids["offgrid"].append(entry_id)

        eve_ids["all"].append(entry_id)

    return ansiblex_destination, counter, eve_ids


def parse(scan_data: list) -> Scan:
    """
    Parse D-Scan

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    # Only parse the d-scan if the module is enabled
    if not AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN:
        raise ParserError(message=_("The D-Scan module is currently disabled."))

    parsed_data = {}
    ansiblex_destination, counter, eve_ids = _get_scan_details(scan_data=scan_data)

    eve_types = EveType.objects.bulk_get_or_create_esi(
        ids=set(eve_ids["all"]), include_children=True
    ).values_list("id", "name", "eve_group__id", "eve_group__name", "mass", named=True)

    # Parse the data parts
    ships = _get_ships(eve_types=eve_types, counter=counter)
    upwell_structures = _get_upwell_structures_on_grid(
        eve_types=eve_types,
        counter=counter,
        ansiblex_destination=ansiblex_destination,
    )
    deployables = _get_deployables_on_grid(eve_types=eve_types, counter=counter)
    starbases = _get_starbases_on_grid(eve_types=eve_types, counter=counter)

    # Add parsed data when available
    sections = {
        "all": (ScanData.Section.SHIPLIST, ships["all"]),
        "ongrid": (ScanData.Section.SHIPLIST_ON_GRID, ships["ongrid"]),
        "offgrid": (ScanData.Section.SHIPLIST_OFF_GRID, ships["offgrid"]),
        "shiptypes": (ScanData.Section.SHIPTYPES, ships["types"]),
        "structures_on_grid": (ScanData.Section.STRUCTURES_ON_GRID, upwell_structures),
        "deployables": (ScanData.Section.DEPLOYABLES_ON_GRID, deployables),
        "starbases": (ScanData.Section.STARBASES_ON_GRID, starbases),
    }

    for key, (section, data) in sections.items():
        if data:
            parsed_data[key] = {"section": section, "data": data}

    return safe_scan_to_db(scan_type=Scan.Type.DSCAN, parsed_data=parsed_data)
