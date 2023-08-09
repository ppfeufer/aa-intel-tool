"""
D-Scan parser
"""

# Standard Library
import re

# Django
from django.db.models import QuerySet
from django.utils.text import slugify
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
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.helper.db import safe_scan_to_db

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def _parse_ship_information(eve_types: QuerySet, counter: dict) -> dict:
    ships = {"all": {}, "ongrid": {}, "offgrid": {}, "types": {}}

    eve_types_ships = eve_types.filter(
        eve_group__eve_category_id__exact=EveCategoryId.SHIP
    )

    for ship_id, ship_name, ship_type_id, ship_type_name in eve_types_ships:
        if ship_id in counter["all"]:
            ships["all"][ship_name] = {
                "id": ship_id,
                "name": ship_name,
                "type_id": ship_type_id,
                "type_name": ship_type_name,
                "type_name_sanitised": slugify(ship_type_name),
                "count": counter["all"][ship_id],
                "image": eveimageserver.type_icon_url(type_id=ship_id, size=32),
            }

            if ship_id in counter["ongrid"]:
                ships["ongrid"][ship_name] = {
                    "id": ship_id,
                    "name": ship_name,
                    "type_id": ship_type_id,
                    "type_name": ship_type_name,
                    "type_name_sanitised": slugify(ship_type_name),
                    "count": counter["ongrid"][ship_id],
                    "image": eveimageserver.type_icon_url(type_id=ship_id, size=32),
                }

            if ship_id in counter["offgrid"]:
                ships["offgrid"][ship_name] = {
                    "id": ship_id,
                    "name": ship_name,
                    "type_id": ship_type_id,
                    "type_name": ship_type_name,
                    "type_name_sanitised": slugify(ship_type_name),
                    "count": counter["offgrid"][ship_id],
                    "image": eveimageserver.type_icon_url(type_id=ship_id, size=32),
                }

    for ship_name, ship_info in ships["all"].items():
        if ship_info["type_name"] not in counter["type"]:
            counter["type"][ship_info["type_name"]] = 0

        counter["type"][ship_info["type_name"]] += ship_info["count"]

        if ship_info["type_name"] not in ships["types"]:
            ships["types"][ship_info["type_name"]] = {
                "name": ship_info["type_name"],
                "name_sanitised": slugify(ship_info["type_name"]),
            }

        ships["types"][ship_info["type_name"]]["count"] = counter["type"][
            ship_info["type_name"]
        ]

    # Sort and clean up the dicts
    cleaned_ships_all = [
        ship
        for (
            ship_name,  # pylint: disable=unused-variable
            ship,
        ) in sorted(ships["all"].items())
    ]
    cleaned_ships_ongrid = [
        ship
        for (
            ship_name,  # pylint: disable=unused-variable
            ship,
        ) in sorted(ships["ongrid"].items())
    ]
    cleaned_ships_offgrid = [
        ship
        for (
            ship_name,  # pylint: disable=unused-variable
            ship,
        ) in sorted(ships["offgrid"].items())
    ]
    cleaned_ships_types = [
        ship
        for (
            ship_name,  # pylint: disable=unused-variable
            ship,
        ) in sorted(ships["types"].items())
    ]

    return {
        "all": cleaned_ships_all,
        "ongrid": cleaned_ships_ongrid,
        "offgrid": cleaned_ships_offgrid,
        "types": cleaned_ships_types,
    }


def parse(scan_data: list) -> tuple:  # pylint: disable=unused-argument
    """
    Parse D-Scan

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    message = _("The D-Scan module is currently disabled.")

    if AppSettings.INTELTOOL_ENABLE_MODULE_DSCAN is True:
        counter = {"all": {}, "ongrid": {}, "offgrid": {}, "type": {}}
        eve_ids = {"all": [], "ongrid": [], "offgrid": []}

        # Let's split this list up
        #
        # [0] => Item ID
        # [1] => Name
        # [2] => Ship Class
        # [3] => Distance
        for entry in scan_data:
            line = re.split(pattern=r"\t+", string=entry.rstrip("\t"))
            entry_id = int(line[0])

            if entry_id not in counter["all"]:
                counter["all"][entry_id] = 0

            if line[3] == "-":
                if entry_id not in counter["offgrid"]:
                    counter["offgrid"][entry_id] = 0

                counter["offgrid"][entry_id] += 1
                eve_ids["offgrid"].append(entry_id)
            else:
                if entry_id not in counter["ongrid"]:
                    counter["ongrid"][entry_id] = 0

                counter["ongrid"][entry_id] += 1
                eve_ids["ongrid"].append(entry_id)

            counter["all"][entry_id] += 1

            eve_ids["all"].append(entry_id)

        eve_types = EveType.objects.bulk_get_or_create_esi(
            ids=set(eve_ids["all"]), include_children=True
        ).values_list("id", "name", "eve_group__id", "eve_group__name")

        # Parse the data
        ships = _parse_ship_information(eve_types=eve_types, counter=counter)

        parsed_data = {
            "shiptypes": {
                "section": ScanData.Section.SHIPTYPES,
                "data": ships["types"],
            },
            "all": {
                "section": ScanData.Section.SHIPLIST,
                "data": ships["all"],
            },
            "ongrid": {
                "section": ScanData.Section.SHIPLIST_ON_GRID,
                "data": ships["ongrid"],
            },
            "offgrid": {
                "section": ScanData.Section.SHIPLIST_OFF_GRID,
                "data": ships["offgrid"],
            },
        }

        return (
            safe_scan_to_db(scan_type=Scan.Type.DSCAN, parsed_data=parsed_data),
            "",
        )

    return None, message
