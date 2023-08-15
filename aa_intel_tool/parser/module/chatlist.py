"""
Chat list parser
"""

# Standard Library
from typing import Union

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
from aa_intel_tool.helper.eve_character import get_or_create_character
from aa_intel_tool.models import Scan, ScanData
from aa_intel_tool.parser.helper.db import safe_scan_to_db

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


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
        alliance_info = _get_unaffiliated_alliance_info()
    else:
        alliance_info = {
            "id": eve_character.alliance_id,
            "name": eve_character.alliance_name,
            "ticker": eve_character.alliance_ticker,
            "logo": eve_character.alliance_logo_url_32,
        }

        if with_evelinks:
            alliance_info["dotlan"] = dotlan.alliance_url(eve_character.alliance_name)
            alliance_info["zkillboard"] = zkillboard.alliance_url(
                eve_character.alliance_id
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

    if with_evelinks:
        corporation_info["dotlan"] = dotlan.corporation_url(
            name=eve_character.corporation_name
        )
        corporation_info["zkillboard"] = zkillboard.alliance_url(
            eve_id=eve_character.corporation_id
        )

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


def _cleanup_entity_data(entity_info: dict) -> list:
    """
    Cleaning up and sorting the parsed entity data

    :param entity_info:
    :type entity_info:
    :return:
    :rtype:
    """

    return [
        data
        for (
            not_used,  # pylint: disable=unused-variable
            data,
        ) in sorted(entity_info.items())
    ]


def _parse_chatscan_data(eve_characters: QuerySet[EveCharacter]) -> dict:
    """
    Parse the chat scan data and return character information,
    corporation information and alliance information for each character

    :param eve_characters:
    :type eve_characters:
    :return:
    :rtype:
    """

    counter = {}
    alliance_info = {}
    corporation_info = {}
    character_info = {}

    for eve_character in eve_characters:
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

        # Character Info
        character_info[eve_character.character_name] = _parse_character_info(
            eve_character=eve_character
        )

        # Update the counter
        counter[eve_character__alliance_name] += 1
        alliance_info[eve_character__alliance_name]["count"] = counter[
            eve_character__alliance_name
        ]

        counter[eve_character.corporation_name] += 1
        corporation_info[eve_character.corporation_name]["count"] = counter[
            eve_character.corporation_name
        ]

    return {
        "pilots": _cleanup_entity_data(entity_info=character_info),
        "corporations": _cleanup_entity_data(entity_info=corporation_info),
        "alliances": _cleanup_entity_data(entity_info=alliance_info),
    }


def parse(scan_data: list, safe_to_db: bool = True) -> Union[Scan, dict]:
    """
    Parse chat list

    This module is hard disabled for now, since CCP can't handle ESI requests and is
    banning IPs that are doing "too many" ESI requests, what ever "too many" means.
    But since we don't want our users getting banned just for using this app, this
    module is currently deactivated and we discourage everyone from activating it in
    the code. Sorry for this, blame CCP's incompetency …

    :param scan_data:
    :type scan_data:
    :param safe_to_db:
    :type safe_to_db:
    :return:
    :rtype:
    """

    message = _("The chat list module is currently disabled.")

    if AppSettings.INTELTOOL_ENABLE_MODULE_CHATSCAN is True:
        logger.debug(msg=f"{len(scan_data)} name(s) to work through …")

        pilots_in_scan = len(scan_data)
        max_allowed_pilots = AppSettings.INTELTOOL_CHATSCAN_MAX_PILOTS

        if 0 < max_allowed_pilots < pilots_in_scan:
            logger.debug(
                msg=(
                    f"Number of pilots in scan ({pilots_in_scan}) exceeds the maximum "
                    f"allowed number ({max_allowed_pilots}). Throwing a tantrum …"
                )
            )

            raise ParserError(
                message=ngettext(
                    singular=f"Chat scans are currently limited to a maximum of {max_allowed_pilots} pilot per scan. Your list of pilots exceeds this limit.",  # pylint: disable=line-too-long
                    plural=f"Chat scans are currently limited to a maximum of {max_allowed_pilots} pilots per scan. Your list of pilots exceeds this limit.",  # pylint: disable=line-too-long
                    number=max_allowed_pilots,
                )
            )

        # Check if we have to bother Eve Universe or if we have all characters already
        # Excluding corporation_id=1000001 (Doomheim) to force an update here …
        fetch_from_eveuniverse = False
        try:
            eve_characters = EveCharacter.objects.filter(
                character_name__in=scan_data
            ).exclude(corporation_id=1000001)
        except EveCharacter.DoesNotExist:  # pylint: disable=no-member
            fetch_from_eveuniverse = True
        else:
            if len(scan_data) != eve_characters.count():
                fetch_from_eveuniverse = True

        if fetch_from_eveuniverse:
            try:
                eve_character_ids = (
                    EveEntity.objects.fetch_by_names_esi(names=scan_data, update=True)
                    .filter(category=EveEntity.CATEGORY_CHARACTER)
                    .values_list("id", flat=True)
                )
            except EveEntity.DoesNotExist as exc:  # pylint: disable=no-member
                message = _(
                    "Something went wrong while fetching the character information from ESI."
                )

                raise ParserError(message=message) from exc

            logger.debug(
                msg=f"Got {len(eve_character_ids)} ID(s) back from Eve Universe …"
            )

            # In case the name does not belong to an Eve character,
            # EveEntity returns an empty object
            if len(eve_character_ids) == 0:
                message = _("Character unknown to ESI.")

                raise ParserError(message=message)

            eve_characters = get_or_create_character(character_ids=eve_character_ids)

        logger.debug(
            msg=f"Got {len(eve_characters)} EveCharacter object(s) back from AA …"
        )

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

        if safe_to_db is False:
            return parsed_data

        return safe_scan_to_db(scan_type=Scan.Type.CHATLIST, parsed_data=parsed_data)

    raise ParserError(message=message)
