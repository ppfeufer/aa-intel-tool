"""
Fleet composition parser
"""

# Standard Library
import re

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.eveonline.evelinks import eveimageserver, evewho, zkillboard
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from eveuniverse.models import EveEntity, EveType

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.app_settings import AppSettings
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.helper.data_structure import dict_to_list
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.helper.db import safe_scan_to_db
from aa_intel_tool.parser.module.chatlist import _get_character_info
from aa_intel_tool.parser.module.chatlist import parse as parse_pilots

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def get_fleet_composition(pilots: dict, ships: dict) -> dict:
    """
    Getting the fleet composition

    :param ships:
    :type ships:
    :return:
    :rtype:
    """

    # Get ship class IDs
    ship_class_ids = (
        EveEntity.objects.fetch_by_names_esi(names=ships["class"], update=True)
        .filter(category=EveEntity.CATEGORY_INVENTORY_TYPE)
        .values_list("id", flat=True)
    )

    # Get ship class details
    ship_class_details = EveType.objects.bulk_get_or_create_esi(
        ids=set(ship_class_ids), include_children=True
    ).values_list("id", "name", "eve_group__id", "eve_group__name", "mass", named=True)

    # Loop through ship classes
    for ship_class in ship_class_details:
        # Build ship class dict
        ships["class"][ship_class.name]["id"] = ship_class.id
        ships["class"][ship_class.name]["name"] = ship_class.name
        ships["class"][ship_class.name]["type_id"] = ship_class.eve_group__id
        ships["class"][ship_class.name]["type_name"] = ship_class.eve_group__name
        ships["class"][ship_class.name]["image"] = eveimageserver.type_icon_url(
            type_id=ship_class.id, size=32
        )
        ships["class"][ship_class.name]["mass"] = (
            ship_class.mass * ships["class"][ship_class.name]["count"]
        )

        # Build ship type dict
        ships["type"][ship_class.eve_group__name]["id"] = ship_class.eve_group__id
        ships["type"][ship_class.eve_group__name]["name"] = ship_class.eve_group__name

    # Pilots
    pilot_details = _get_character_info(scan_data=list(set(pilots)))

    # Loop through pilots
    for pilot in pilot_details:
        # Get ship class details for a pilot
        pilot__ship_class = ship_class_details.filter(
            name=pilots[pilot.character_name]["ship"]
        ).get()

        # Build pilots dict
        pilots[pilot.character_name]["id"] = pilot.character_id
        pilots[pilot.character_name]["portrait"] = pilot.portrait_url_32
        pilots[pilot.character_name]["evewho"] = evewho.character_url(
            pilot.character_id
        )
        pilots[pilot.character_name]["zkillboard"] = zkillboard.character_url(
            pilot.character_id
        )
        pilots[pilot.character_name]["ship_id"] = pilot__ship_class.id
        pilots[pilot.character_name]["ship_type_id"] = pilot__ship_class.eve_group__id

    return {
        "classes": dict_to_list(input_dict=ships["class"]),
        "types": dict_to_list(input_dict=ships["type"]),
        "pilots": dict_to_list(input_dict=pilots),
    }


def parse_line(line) -> list:
    """
    Parse a line from the fleet composition scan

    :param line:
    :type line:
    :return:
    :rtype:
    """

    # Let's split this list up
    #
    # line[0] => Pilot Name
    # line[1] => System
    # line[2] => Ship Class
    # line[3] => Ship Type
    # line[4] => Position in Fleet
    # line[5] => Skills (FC - WC - SC)
    # line[6] => Wing Name / Squad Name
    line = re.split(pattern=r"\t+", string=line.rstrip("\t"))

    if len(line) == 6:
        line.append("")

    return line


def update_ships(ships, line) -> dict:
    """
    Update the ships dict

    :param ships:
    :type ships:
    :param line:
    :type line:
    :return:
    :rtype:
    """

    if line[2] not in ships["class"]:
        ships["class"][line[2]] = {"count": 0}

    if line[3] not in ships["type"]:
        ships["type"][line[3]] = {"count": 0}

    ships["class"][line[2]]["count"] += 1
    ships["type"][line[3]]["count"] += 1

    return ships


def handle_fleet_composition_and_participation(pilots, ships) -> tuple:
    """
    Handle the fleet composition and participation

    :param pilots:
    :type pilots:
    :param ships:
    :type ships:
    :return:
    :rtype:
    """

    fleet_composition = get_fleet_composition(pilots=pilots, ships=ships)
    participation = None

    if AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN is True:
        participation = parse_pilots(
            scan_data=list(set(pilots)),
            safe_to_db=False,
            ignore_limit=True,
        )

    return fleet_composition, participation


def parse(scan_data: list) -> Scan:
    """
    Parse the fleet composition scan

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    message = _("The fleet composition module is currently disabled.")

    if AppSettings.INTELTOOL_ENABLE_MODULE_FLEETCOMP is True:
        parsed_data = {}
        pilots = {}
        ships = {"type": {}, "class": {}}
        lines = []

        # Loop through the scan data
        for entry in scan_data:
            line = parse_line(entry)

            pilots[line[0]] = {
                "name": line[0],
                "solarsystem": line[1],
                "ship": line[2],
                "ship_type": line[3],
            }
            ships = update_ships(ships=ships, line=line)

            lines.append(line)

        fleet_composition, participation = handle_fleet_composition_and_participation(
            pilots=pilots, ships=ships
        )

        logger.debug(msg=fleet_composition)

        # Add "ship classes" to parsed data when available
        if fleet_composition["classes"]:
            parsed_data["classes"] = {
                "section": ScanData.Section.SHIPLIST,
                "data": fleet_composition["classes"],
            }

        # Add "ship types" to parsed data when available
        if fleet_composition["types"]:
            parsed_data["shiptypes"] = {
                "section": ScanData.Section.SHIPTYPES,
                "data": fleet_composition["types"],
            }

        # Add "who is flying what" (the actual fleet composition) to parsed data when available
        if fleet_composition["pilots"]:
            parsed_data["pilots_flying"] = {
                "section": ScanData.Section.FLEETCOMPOSITION,
                "data": fleet_composition["pilots"],
            }

        # Add fleet participation data to the parsed data
        if participation:
            parsed_data.update(participation)

        return safe_scan_to_db(scan_type=Scan.Type.FLEETCOMP, parsed_data=parsed_data)

    raise ParserError(message=message)
