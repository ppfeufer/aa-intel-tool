"""
Chat list parser
"""

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from eveuniverse.models import EveEntity

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.helper.eve_character import get_or_create_character
from aa_intel_tool.models import Scan

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def parse(scan_data: list) -> tuple:
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

        if eve_character.alliance_id is None:
            eve_character__alliance_id = 1

            if "unaffiliated" not in counter:
                counter["unaffiliated"] = 0

            counter["unaffiliated"] += 1
            alliance_info[1] = {
                "id": 1,
                "name": str(_("Unaffiliated / No Alliance")),
                "ticker": "",
                "count": counter["unaffiliated"],
            }
        else:
            eve_character__alliance_id = eve_character.alliance_id

            if eve_character__alliance_id not in counter:
                counter[eve_character__alliance_id] = 0

            counter[eve_character__alliance_id] += 1
            alliance_info[eve_character__alliance_id] = {
                "id": eve_character__alliance_id,
                "name": eve_character.alliance_name,
                "ticker": eve_character.alliance_ticker,
                "count": counter[eve_character__alliance_id],
            }

        if eve_character.corporation_id not in counter:
            counter[eve_character.corporation_id] = 0

        counter[eve_character.corporation_id] += 1
        corporation_info[eve_character.corporation_id] = {
            "id": eve_character.corporation_id,
            "name": eve_character.corporation_name,
            "ticker": eve_character.corporation_ticker,
            "count": counter[eve_character.corporation_id],
            "alliance": alliance_info[eve_character__alliance_id],
        }

        character_info[eve_character.character_id] = {
            "id": eve_character.character_id,
            "name": eve_character.character_name,
            "corporation": corporation_info[eve_character.corporation_id],
            "alliance": alliance_info[eve_character__alliance_id],
        }

    scan_data = {
        "pilots": character_info,
        "corporations": corporation_info,
        "alliances": alliance_info,
    }

    return Scan.Type.CHATLIST, scan_data
