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
from aa_intel_tool.app_settings import AppSettings
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

    if re.search(pattern=REGEX_PATTERN["localised_on_grid"], string=distance):
        # line = re.split(pattern=r" ", string=distance)
        distance_sanitised = int(re.sub(r"[^0-9]", "", distance))

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

    eve_types_ships = eve_types.filter(
        eve_group__eve_category_id__exact=EveCategoryId.SHIP
    )

    for eve_type in eve_types_ships:
        # Info for "All Ships" table
        if eve_type[0] in counter["all"]:
            if eve_type[1] not in ships["all"]:
                ships["all"][eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
                ships["all"][eve_type[1]]["count"] = counter["all"][eve_type[0]]

        # Info for "On Grid" table
        if eve_type[0] in counter["ongrid"]:
            if eve_type[1] not in ships["ongrid"]:
                ships["ongrid"][eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
                ships["ongrid"][eve_type[1]]["count"] = counter["ongrid"][eve_type[0]]

        # Info for "Off Grid" table
        if eve_type[0] in counter["offgrid"]:
            if eve_type[1] not in ships["offgrid"]:
                ships["offgrid"][eve_type[1]] = _get_type_info_dict(eve_type=eve_type)
                ships["offgrid"][eve_type[1]]["count"] = counter["offgrid"][eve_type[0]]

        # Info for "Ship Types" table
        if eve_type[3] not in ships["types"]:
            ships["types"][eve_type[3]] = {
                "id": eve_type[2],
                "name": eve_type[3],
                "count": 0,
            }

        # Add the count to the ship types
        ships["types"][eve_type[3]]["count"] += counter["all"][eve_type[0]]

    # Leaving this here just in case the method in the first loop turns out to be faulty
    # for ship_name, ship_info in ships["all"].items():  # pylint: disable=unused-variable
    #     if ship_info["type_name"] not in counter["type"]:
    #         counter["type"][ship_info["type_name"]] = 0
    #
    #     counter["type"][ship_info["type_name"]] += ship_info["count"]
    #
    #     if ship_info["type_name"] not in ships["types"]:
    #         ships["types"][ship_info["type_name"]] = {
    #             "name": ship_info["type_name"],
    #             "name_sanitised": slugify(ship_info["type_name"]),
    #         }
    #
    #     ships["types"][ship_info["type_name"]]["count"] = counter["type"][
    #         ship_info["type_name"]
    #     ]

    return {
        "all": dict_to_list(input_dict=ships["all"]),
        "ongrid": dict_to_list(input_dict=ships["ongrid"]),
        "offgrid": dict_to_list(input_dict=ships["offgrid"]),
        "types": dict_to_list(input_dict=ships["types"]),
    }


def _get_upwell_structures_on_grid(eve_types: QuerySet, dscan_list: list) -> list:
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

    structures_on_grid = {}

    for item in dscan_list:
        if eve_types_structures.filter(id=item[0]).exists() and _is_on_grid(item[3]):
            if item[0] not in structures_on_grid:
                structures_on_grid[item[0]] = {
                    "id": item[0],
                    "type": item[2],
                    "count": 0,
                }

            structures_on_grid[item[0]]["count"] += 1

    return dict_to_list(structures_on_grid)


def parse(scan_data: list) -> Scan:
    """
    Parse D-Scan

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    message = _("The D-Scan module is currently disabled.")

    if AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN is True:
        # AA Intel Tool
        from aa_intel_tool.constants import (  # pylint: disable=import-outside-toplevel
            REGEX_PATTERN,
        )

        counter = {"all": {}, "ongrid": {}, "offgrid": {}, "type": {}}
        eve_ids = {"all": [], "ongrid": [], "offgrid": []}
        dscan_lines = []
        parsed_data = {}

        # Let's split this list up
        #
        # [0] => Item ID
        # [1] => Name
        # [2] => Ship Class / Structure Type
        # [3] => Distance
        for entry in scan_data:
            line = re.split(pattern=r"\t+", string=entry.rstrip("\t"))
            entry_id = int(line[0])

            if entry_id not in counter["all"]:
                counter["all"][entry_id] = 0

            if re.search(pattern=REGEX_PATTERN["localised_on_grid"], string=line[3]):
                if entry_id not in counter["ongrid"]:
                    counter["ongrid"][entry_id] = 0

                counter["ongrid"][entry_id] += 1
                eve_ids["ongrid"].append(entry_id)
            else:
                if entry_id not in counter["offgrid"]:
                    counter["offgrid"][entry_id] = 0

                counter["offgrid"][entry_id] += 1
                eve_ids["offgrid"].append(entry_id)

            counter["all"][entry_id] += 1
            eve_ids["all"].append(entry_id)
            dscan_lines.append([entry_id, line[1], line[2], line[3]])

        eve_types = EveType.objects.bulk_get_or_create_esi(
            ids=set(eve_ids["all"]), include_children=True
        ).values_list("id", "name", "eve_group__id", "eve_group__name", named=True)

        # Parse the data
        ships = _get_ships(eve_types=eve_types, counter=counter)
        upwell_structures = _get_upwell_structures_on_grid(
            eve_types=eve_types, dscan_list=dscan_lines
        )

        # Add "ship types" to parsed data when available
        if len(ships["types"]):
            parsed_data["shiptypes"] = {
                "section": ScanData.Section.SHIPTYPES,
                "data": ships["types"],
            }

        # Add "ships all" to parsed data when available
        if len(ships["all"]):
            parsed_data["all"] = {
                "section": ScanData.Section.SHIPLIST,
                "data": ships["all"],
            }

        # Add "ships on grid" to parsed data when available
        if len(ships["ongrid"]):
            parsed_data["ongrid"] = {
                "section": ScanData.Section.SHIPLIST_ON_GRID,
                "data": ships["ongrid"],
            }

        # Add "ships off grid" to parsed data when available
        if len(ships["offgrid"]):
            parsed_data["offgrid"] = {
                "section": ScanData.Section.SHIPLIST_OFF_GRID,
                "data": ships["offgrid"],
            }

        # Add "Upwell structures on grid" to parsed data when available
        if len(upwell_structures):
            parsed_data["sructures_on_grid"] = {
                "section": ScanData.Section.STRUCTURES_ON_GRID,
                "data": upwell_structures,
            }

        return safe_scan_to_db(scan_type=Scan.Type.DSCAN, parsed_data=parsed_data)

    raise ParserError(message=message)
