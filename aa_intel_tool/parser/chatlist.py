"""
Chat list parser
"""

# Alliance Auth
from allianceauth.eveonline.evelinks import dotlan, eveimageserver, evewho, zkillboard
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from eveuniverse.models import EveEntity

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.helper.eve_character import get_or_create_character
from aa_intel_tool.models import Scan

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def parse(  # pylint: disable=too-many-locals, too-many-branches
    scan_data: list,
) -> tuple:
    """
    Parse chat list

    :param scan_data:
    :type scan_data:
    :return:
    :rtype:
    """

    logger.debug(msg=scan_data)

    try:
        eve_character_ids = (
            EveEntity.objects.fetch_by_names_esi(names=scan_data)
            .filter(category=EveEntity.CATEGORY_CHARACTER)
            .values_list("id", flat=True)
        )
    except EveEntity.DoesNotExist:  # pylint: disable=no-member
        return Scan.Type.CHATLIST, None

    logger.debug(msg=eve_character_ids)

    if eve_character_ids.count() == 0:
        return Scan.Type.CHATLIST, None

    counter = {}
    alliance_info = {}
    corporation_info = {}
    character_info = {}

    for character_id in eve_character_ids:
        eve_character = get_or_create_character(character_id=character_id)

        eve_character__alliance_id = 1
        if eve_character.alliance_id is None:
            if eve_character__alliance_id not in counter:
                counter[eve_character__alliance_id] = 0

            counter[eve_character__alliance_id] += 1

            if eve_character__alliance_id not in alliance_info:
                alliance_info[eve_character__alliance_id] = {
                    "id": eve_character__alliance_id,
                    "name": "",
                    "ticker": "",
                    "logo": eveimageserver.alliance_logo_url(
                        alliance_id=eve_character__alliance_id, size=32
                    ),
                }
        else:
            eve_character__alliance_id = eve_character.alliance_id

            if eve_character__alliance_id not in counter:
                counter[eve_character__alliance_id] = 0

            counter[eve_character__alliance_id] += 1

            if eve_character__alliance_id not in alliance_info:
                alliance_info[eve_character__alliance_id] = {
                    "id": eve_character__alliance_id,
                    "name": eve_character.alliance_name,
                    "ticker": eve_character.alliance_ticker,
                    "logo": eveimageserver.alliance_logo_url(
                        alliance_id=eve_character__alliance_id, size=32
                    ),
                    "dotlan": dotlan.alliance_url(eve_character.alliance_name),
                    "zkillboard": zkillboard.alliance_url(eve_character__alliance_id),
                }

        alliance_info[eve_character__alliance_id]["count"] = counter[
            eve_character__alliance_id
        ]

        if eve_character.corporation_id not in counter:
            counter[eve_character.corporation_id] = 0

        counter[eve_character.corporation_id] += 1
        corporation_info[eve_character.corporation_id] = {
            "id": eve_character.corporation_id,
            "name": eve_character.corporation_name,
            "ticker": eve_character.corporation_ticker,
            "logo": eveimageserver.corporation_logo_url(
                corporation_id=eve_character.corporation_id, size=32
            ),
            "dotlan": dotlan.corporation_url(eve_character.corporation_name),
            "zkillboard": zkillboard.corporation_url(eve_character.corporation_id),
            "count": counter[eve_character.corporation_id],
            "alliance": alliance_info[eve_character__alliance_id],
        }

        character_info[eve_character.character_id] = {
            "id": eve_character.character_id,
            "name": eve_character.character_name,
            "portrait": eveimageserver.character_portrait_url(
                character_id=eve_character.character_id, size=32
            ),
            "evewho": evewho.character_url(eve_character.character_id),
            "zkillboard": zkillboard.character_url(eve_character.character_id),
            "corporation": corporation_info[eve_character.corporation_id],
            "alliance": alliance_info[eve_character__alliance_id],
        }

    # Clean up the dicts
    cleaned_pilot_data = []
    cleaned_corporation_data = []
    cleaned_alliance_data = []
    for (
        character_id,  # pylint: disable=unused-variable
        character,
    ) in character_info.items():
        cleaned_pilot_data.append(character)

    for (
        corporation_id,  # pylint: disable=unused-variable
        corporation,
    ) in corporation_info.items():
        cleaned_corporation_data.append(corporation)

    for (
        alliance_id,  # pylint: disable=unused-variable
        alliance,
    ) in alliance_info.items():
        cleaned_alliance_data.append(alliance)

    scan_data = {
        "pilots": cleaned_pilot_data,
        "corporations": cleaned_corporation_data,
        "alliances": cleaned_alliance_data,
    }

    return Scan.Type.CHATLIST, scan_data
