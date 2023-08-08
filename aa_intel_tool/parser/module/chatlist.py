"""
Chat list parser
"""

# Alliance Auth
from allianceauth.eveonline.evelinks import dotlan, eveimageserver, evewho, zkillboard
from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from eveuniverse.models import EveEntity

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.app_settings import AppSettings
from aa_intel_tool.helper.eve_character import get_or_create_character
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.helper.db import safe_scan_to_db

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def _parse_alliance_info(eve_character: EveCharacter) -> dict:
    """
    Parse the alliance information from an EveCharacter

    :param eve_character:
    :type eve_character:
    :return:
    :rtype:
    """

    if eve_character.alliance_id is None:
        alliance_info = {
            "id": 1,
            "name": "",
            "ticker": "",
            "logo": eveimageserver.alliance_logo_url(alliance_id=1, size=32),
        }
    else:
        alliance_info = {
            "id": eve_character.alliance_id,
            "name": eve_character.alliance_name,
            "ticker": eve_character.alliance_ticker,
            "logo": eveimageserver.alliance_logo_url(
                alliance_id=eve_character.alliance_id, size=32
            ),
            "dotlan": dotlan.alliance_url(eve_character.alliance_name),
            "zkillboard": zkillboard.alliance_url(eve_character.alliance_id),
        }

    return alliance_info


def _parse_corporation_info(eve_character: EveCharacter) -> dict:
    """
    Parse the corporation information from an EveCharacter

    :param eve_character:
    :type eve_character:
    :return:
    :rtype:
    """

    return {
        "id": eve_character.corporation_id,
        "name": eve_character.corporation_name,
        "ticker": eve_character.corporation_ticker,
        "logo": eveimageserver.corporation_logo_url(
            corporation_id=eve_character.corporation_id, size=32
        ),
        "dotlan": dotlan.corporation_url(eve_character.corporation_name),
        "zkillboard": zkillboard.corporation_url(eve_character.corporation_id),
    }


def _parse_character_info(eve_character: EveCharacter) -> dict:
    """
    Parse the character information from an EveCharacter

    :param eve_character:
    :type eve_character:
    :return:
    :rtype:
    """

    return {
        "id": eve_character.character_id,
        "name": eve_character.character_name,
        "portrait": eveimageserver.character_portrait_url(
            character_id=eve_character.character_id, size=32
        ),
        "evewho": evewho.character_url(eve_character.character_id),
        "zkillboard": zkillboard.character_url(eve_character.character_id),
    }


def parse(scan_data: list, safe_to_db: bool = True):
    """
    Parse chat list

    :param scan_data:
    :type scan_data:
    :param safe_to_db:
    :type safe_to_db:
    :return:
    :rtype:
    """

    if AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN is False:
        return None

    logger.debug(msg=scan_data)

    try:
        eve_character_ids = (
            EveEntity.objects.fetch_by_names_esi(names=scan_data)
            .filter(category=EveEntity.CATEGORY_CHARACTER)
            .values_list("id", flat=True)
        )
    except EveEntity.DoesNotExist:  # pylint: disable=no-member
        return None

    logger.debug(msg=eve_character_ids)

    # In case the name does not belong to an Eve character,
    # # EveEntity returns an empty object
    if eve_character_ids.count() == 0:
        return None

    counter = {}
    alliance_info = {}
    corporation_info = {}
    character_info = {}

    # Loop through the list of character IDs
    for character_id in eve_character_ids:
        eve_character = get_or_create_character(character_id=character_id)

        eve_character__alliance_name = "Unaffiliated"
        if eve_character.alliance_name is not None:
            eve_character__alliance_name = eve_character.alliance_name

        if eve_character__alliance_name not in counter:
            counter[eve_character__alliance_name] = 0

        if eve_character.corporation_name not in counter:
            counter[eve_character.corporation_name] = 0

        # Alliance Info
        if eve_character__alliance_name not in alliance_info:
            alliance_info[eve_character__alliance_name] = _parse_alliance_info(
                eve_character=eve_character
            )

        # Corporation Info
        if eve_character.corporation_name not in corporation_info:
            corporation_info[eve_character.corporation_name] = _parse_corporation_info(
                eve_character=eve_character
            )
            corporation_info[eve_character.corporation_name][
                "alliance"
            ] = alliance_info[eve_character__alliance_name]

        # Character Info
        character_info[eve_character.character_name] = _parse_character_info(
            eve_character=eve_character
        )
        character_info[eve_character.character_name]["corporation"] = corporation_info[
            eve_character.corporation_name
        ]
        character_info[eve_character.character_name]["alliance"] = alliance_info[
            eve_character__alliance_name
        ]

        # Update the counter
        counter[eve_character__alliance_name] += 1
        alliance_info[eve_character__alliance_name]["count"] = counter[
            eve_character__alliance_name
        ]

        counter[eve_character.corporation_name] += 1
        corporation_info[eve_character.corporation_name]["count"] = counter[
            eve_character.corporation_name
        ]

    # Sort and clean up the dicts
    cleaned_pilot_data = [
        character
        for (
            character_name,  # pylint: disable=unused-variable
            character,
        ) in sorted(character_info.items())
    ]
    cleaned_corporation_data = [
        corporation
        for (
            corporation_name,  # pylint: disable=unused-variable
            corporation,
        ) in sorted(corporation_info.items())
    ]
    cleaned_alliance_data = [
        alliance
        for (
            alliance_name,  # pylint: disable=unused-variable
            alliance,
        ) in sorted(alliance_info.items())
    ]

    parsed_data = {
        "pilots": {
            "section": ScanData.Section.PILOTLIST,
            "data": cleaned_pilot_data,
        },
        "corporations": {
            "section": ScanData.Section.CORPORATIONLIST,
            "data": cleaned_corporation_data,
        },
        "alliances": {
            "section": ScanData.Section.ALLIANCELIST,
            "data": cleaned_alliance_data,
        },
    }

    if safe_to_db is False:
        return parsed_data

    return safe_scan_to_db(scan_type=Scan.Type.CHATLIST, parsed_data=parsed_data)
