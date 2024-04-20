"""
D-Scan parser
"""

# Standard Library
import re

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
    if re.search(pattern=REGEX_PATTERN["localised_on_grid"], string=distance):
        distance_sanitised = int(re.sub(pattern=r"[^0-9]", repl="", string=distance))

        # Check if the distance is within the grid size
        if distance_sanitised <= AppSettings.INTELTOOL_DSCAN_GRID_SIZE:
            return True

        return False

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
    for eve_type in eve_types_ships:
        # Info for "All Ships" table
        if eve_type[0] in counter["all"]:
            if eve_type[1] not in ships["all"]:
                ships["all"][eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
                ships["all"][eve_type[1]]["count"] = counter["all"][eve_type[0]]
                ships["all"][eve_type[1]]["mass"] = (
                    eve_type[4] * counter["all"][eve_type[0]]
                )

        # Info for "On Grid" table
        if eve_type[0] in counter["ongrid"]:
            if eve_type[1] not in ships["ongrid"]:
                ships["ongrid"][eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
                ships["ongrid"][eve_type[1]]["count"] = counter["ongrid"][eve_type[0]]
                ships["ongrid"][eve_type[1]]["mass"] = (
                    eve_type[4] * counter["ongrid"][eve_type[0]]
                )

        # Info for "Off Grid" table
        if eve_type[0] in counter["offgrid"]:
            if eve_type[1] not in ships["offgrid"]:
                ships["offgrid"][eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
                ships["offgrid"][eve_type[1]]["count"] = counter["offgrid"][eve_type[0]]
                ships["offgrid"][eve_type[1]]["mass"] = (
                    eve_type[4] * counter["offgrid"][eve_type[0]]
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

    upwell_structures = {}

    # Loop through all Upwell structures
    for eve_type in eve_types_structures:
        if eve_type[0] in counter["ongrid"]:
            if eve_type[1] not in upwell_structures:
                upwell_structures[eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
                upwell_structures[eve_type[1]]["count"] = counter["ongrid"][eve_type[0]]

                # If it is an Ansiblex Jump Gate, add the destination system
                if (
                    eve_type[0] == UpwellStructureId.ANSIBLEX_JUMP_GATE
                    and ansiblex_destination
                ):
                    upwell_structures[eve_type[1]][
                        "name"
                    ] += f" » {ansiblex_destination}"

    return dict_to_list(upwell_structures)


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

    deployables = {}

    # Loop through all deployables
    for eve_type in eve_types_deployables:
        if eve_type[0] in counter["ongrid"]:
            if eve_type[1] not in deployables:
                deployables[eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
                deployables[eve_type[1]]["count"] = counter["ongrid"][eve_type[0]]

    return dict_to_list(deployables)


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

    starbases = {}

    # Loop through all starbases
    for eve_type in eve_types_starbase:
        if eve_type[0] in counter["ongrid"]:
            if eve_type[1] not in starbases:
                starbases[eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
                starbases[eve_type[1]]["count"] = counter["ongrid"][eve_type[0]]

    return dict_to_list(starbases)


def _get_ansiblex_jumpgate_destination(ansiblex_name: str) -> str:
    """
    Get the Ansiblex Jump Gate destination system

    :param ansiblex_name:
    :type ansiblex_name:
    :return:
    :rtype:
    """

    name_parts = re.split(pattern=r" - ", string=ansiblex_name)
    gate_systems = re.split(pattern=r" » ", string=name_parts[0])

    return gate_systems[1]


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
    counter = {"all": {}, "ongrid": {}, "offgrid": {}, "type": {}}
    eve_ids = {"all": [], "ongrid": [], "offgrid": []}

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

        counter["all"][entry_id] = counter["all"].get(entry_id, 0) + 1

        # Check if the entry is "on grid" or not
        if _is_on_grid(line.group(4)):
            counter["ongrid"][entry_id] = counter["ongrid"].get(entry_id, 0) + 1

            # If it is an Ansiblex Jump Gate, get its destination system
            if entry_id == UpwellStructureId.ANSIBLEX_JUMP_GATE:
                ansiblex_destination = _get_ansiblex_jumpgate_destination(
                    ansiblex_name=line.group(2)
                )

            eve_ids["ongrid"].append(entry_id)
        else:
            counter["offgrid"][entry_id] = counter["offgrid"].get(entry_id, 0) + 1

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

    message = _("The D-Scan module is currently disabled.")

    # Only parse the D-Scan when the module is enabled
    if AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN is True:
        parsed_data = {}
        (
            ansiblex_destination,  # pylint: disable=unused-variable
            counter,
            eve_ids,
        ) = _get_scan_details(scan_data=scan_data)

        eve_types = EveType.objects.bulk_get_or_create_esi(
            ids=set(eve_ids["all"]), include_children=True
        ).values_list(
            "id", "name", "eve_group__id", "eve_group__name", "mass", named=True
        )

        # Parse the data parts
        ships = _get_ships(eve_types=eve_types, counter=counter)
        upwell_structures = _get_upwell_structures_on_grid(
            eve_types=eve_types,
            counter=counter,
            # ansiblex_destination=ansiblex_destination,
        )
        deployables = _get_deployables_on_grid(eve_types=eve_types, counter=counter)
        starbases = _get_starbases_on_grid(eve_types=eve_types, counter=counter)

        # Add "ships all" to the parsed data when available
        if ships["all"]:
            parsed_data["all"] = {
                "section": ScanData.Section.SHIPLIST,
                "data": ships["all"],
            }

        # Add "ships on grid" to the parsed data when available
        if ships["ongrid"]:
            parsed_data["ongrid"] = {
                "section": ScanData.Section.SHIPLIST_ON_GRID,
                "data": ships["ongrid"],
            }

        # Add "ships off grid" to parsed data when available
        if ships["offgrid"]:
            parsed_data["offgrid"] = {
                "section": ScanData.Section.SHIPLIST_OFF_GRID,
                "data": ships["offgrid"],
            }

        # Add "ship types" to the parsed data when available
        if ships["types"]:
            parsed_data["shiptypes"] = {
                "section": ScanData.Section.SHIPTYPES,
                "data": ships["types"],
            }

        # Add "Upwell structures on grid" to the parsed data when available
        if upwell_structures:
            parsed_data["sructures_on_grid"] = {
                "section": ScanData.Section.STRUCTURES_ON_GRID,
                "data": upwell_structures,
            }

        # Add "deployables on grid" to the parsed data when available
        if deployables:
            parsed_data["deployables"] = {
                "section": ScanData.Section.DEPLOYABLES_ON_GRID,
                "data": deployables,
            }

        # Add "starbases on grid" to parsed data when available
        if starbases:
            parsed_data["starbases"] = {
                "section": ScanData.Section.STARBASES_ON_GRID,
                "data": starbases,
            }

        return safe_scan_to_db(scan_type=Scan.Type.DSCAN, parsed_data=parsed_data)

    raise ParserError(message=message)
