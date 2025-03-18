"""
Chat list parser
"""

# Standard Library
from collections import defaultdict

# Django
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

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
from aa_intel_tool.exceptions import ParserError
from aa_intel_tool.helper.data_structure import dict_to_list
from aa_intel_tool.helper.eve_character import get_or_create_character
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.helper.db import safe_scan_to_db

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def _get_character_info(scan_data: list) -> QuerySet[EveCharacter]:
    """
    Get Eve character information and affiliation from a list of character names

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    # Excluding corporation_id=1000001 (Doomheim) to potentially force an update here …
    eve_characters = EveCharacter.objects.filter(character_name__in=scan_data).exclude(
        corporation_id=1000001
    )

    # Check if we have to bother Eve Universe or if we have all characters already
    if len(scan_data) != eve_characters.count():
        try:
            eve_character_ids = (
                EveEntity.objects.fetch_by_names_esi(names=scan_data, update=True)
                .filter(category=EveEntity.CATEGORY_CHARACTER)
                .values_list("id", flat=True)
            )
        except EveEntity.DoesNotExist as exc:  # pylint: disable=no-member
            raise ParserError(
                message=_(
                    "Something went wrong while fetching the character information from ESI."
                )
            ) from exc

        # In case the name does not belong to an Eve character,
        # EveEntity returns an empty object
        if not eve_character_ids:
            raise ParserError(message=_("Character unknown to ESI."))

        eve_characters = get_or_create_character(character_ids=eve_character_ids)

    return eve_characters


def _get_unaffiliated_alliance_info() -> dict:
    """
    Get the alliance_info dict for characters that are in no alliance

    :return:
    :rtype:
    """

    return {
        "id": 1,
        "name": "",
        "ticker": "",
        "logo": eveimageserver.alliance_logo_url(alliance_id=1, size=32),
    }


def _parse_alliance_info(
    eve_character: EveCharacter, with_evelinks: bool = True
) -> dict:
    """
    Parse the alliance information from an EveCharacter

    :param eve_character:
    :type eve_character:
    :return:
    :rtype:
    """

    if eve_character.alliance_id is None:
        return _get_unaffiliated_alliance_info()

    alliance_info = {
        "id": eve_character.alliance_id,
        "name": eve_character.alliance_name,
        "ticker": eve_character.alliance_ticker,
        "logo": eve_character.alliance_logo_url_32,
    }

    # Add eve links if requested
    if with_evelinks:
        alliance_info.update(
            {
                "dotlan": dotlan.alliance_url(eve_character.alliance_name),
                "zkillboard": zkillboard.alliance_url(eve_character.alliance_id),
            }
        )

    return alliance_info


def _parse_corporation_info(
    eve_character: EveCharacter,
    with_alliance_info: bool = True,
    with_evelinks: bool = True,
) -> dict:
    """
    Parse the corporation information from an EveCharacter

    :param eve_character:
    :type eve_character:
    :return:
    :rtype:
    """

    corporation_info = {
        "id": eve_character.corporation_id,
        "name": eve_character.corporation_name,
        "ticker": eve_character.corporation_ticker,
        "logo": eve_character.corporation_logo_url_32,
    }

    # Add eve links if requested
    if with_evelinks:
        corporation_info.update(
            {
                "dotlan": dotlan.corporation_url(name=eve_character.corporation_name),
                "zkillboard": zkillboard.corporation_url(
                    eve_id=eve_character.corporation_id
                ),
            }
        )

    # Add alliance info if requested
    if with_alliance_info:
        corporation_info["alliance"] = _parse_alliance_info(
            eve_character=eve_character, with_evelinks=with_evelinks
        )

    return corporation_info


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
        "portrait": eve_character.portrait_url_32,
        "evewho": evewho.character_url(eve_character.character_id),
        "zkillboard": zkillboard.character_url(eve_character.character_id),
        "corporation": _parse_corporation_info(
            eve_character=eve_character, with_alliance_info=False, with_evelinks=False
        ),
        "alliance": _parse_alliance_info(
            eve_character=eve_character, with_evelinks=False
        ),
    }


def _parse_chatscan_data(eve_characters: QuerySet[EveCharacter]) -> dict:
    """
    Parse the chat scan data and return character information,
    corporation information and alliance information for each character

    :param eve_characters:
    :type eve_characters:
    :return:
    :rtype:
    """

    counter = defaultdict(int)
    alliance_info = {}
    corporation_info = {}
    character_info = {}

    # Loop through the characters
    for eve_character in list(eve_characters):
        alliance_name = eve_character.alliance_name or "Unaffiliated"
        corporation_name = eve_character.corporation_name

        counter[alliance_name] += 1
        counter[corporation_name] += 1

        # Alliance Info
        if alliance_name not in alliance_info:
            alliance_info[alliance_name] = _parse_alliance_info(eve_character)

        # Corporation Info
        if corporation_name not in corporation_info:
            corporation_info[corporation_name] = _parse_corporation_info(eve_character)

        # Character Info
        character_info[eve_character.character_name] = _parse_character_info(
            eve_character
        )

        # Update the counter
        alliance_info[alliance_name]["count"] = counter[alliance_name]
        corporation_info[corporation_name]["count"] = counter[corporation_name]

    return {
        "pilots": dict_to_list(input_dict=character_info),
        "corporations": dict_to_list(input_dict=corporation_info),
        "alliances": dict_to_list(input_dict=alliance_info),
    }


def parse(
    scan_data: list, safe_to_db: bool = True, ignore_limit: bool = False
) -> Scan | dict:
    """
    Parse chat list

    :param scan_data:
    :type scan_data:
    :param safe_to_db:
    :type safe_to_db:
    :param ignore_limit:
    :type ignore_limit:
    :return:
    :rtype:
    """

    # Only parse the chat scan if the module is enabled
    if not AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN:
        raise ParserError(message=_("The chat list module is currently disabled."))

    logger.debug(msg=f"{len(scan_data)} name(s) to work through …")

    pilots_in_scan = len(scan_data)
    max_allowed_pilots = AppSettings.INTELTOOL_CHATSCAN_MAX_PILOTS

    # Check if the number of pilots in the scan exceeds the maximum allowed number
    if 0 < max_allowed_pilots < pilots_in_scan and not ignore_limit:
        logger.debug(
            msg=(
                f"Number of pilots in scan ({pilots_in_scan}) exceeds the maximum "
                f"allowed number ({max_allowed_pilots}). Throwing a tantrum …"
            )
        )

        # Throw a tantrum
        raise ParserError(
            message=ngettext(
                singular=f"Chat scans are currently limited to a maximum of {max_allowed_pilots} pilot per scan. Your list of pilots exceeds this limit.",
                plural=f"Chat scans are currently limited to a maximum of {max_allowed_pilots} pilots per scan. Your list of pilots exceeds this limit.",
                number=max_allowed_pilots,
            )
        )

    eve_characters = _get_character_info(scan_data=scan_data)
    logger.debug(msg=f"Got {len(eve_characters)} EveCharacter object(s) back from AA …")

    # Parse the data
    parsed_chatscan = _parse_chatscan_data(eve_characters=eve_characters)
    parsed_data = {
        "pilots": {
            "section": ScanData.Section.PILOTLIST,
            "data": parsed_chatscan["pilots"],
        },
        "corporations": {
            "section": ScanData.Section.CORPORATIONLIST,
            "data": parsed_chatscan["corporations"],
        },
        "alliances": {
            "section": ScanData.Section.ALLIANCELIST,
            "data": parsed_chatscan["alliances"],
        },
    }

    return (
        parsed_data
        if not safe_to_db
        else safe_scan_to_db(scan_type=Scan.Type.CHATLIST, parsed_data=parsed_data)
    )
