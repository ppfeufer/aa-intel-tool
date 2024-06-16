"""
Little helper functions to deal with Eve characters
"""

# Standard Library
from collections.abc import Iterable

# Django
from django.db.models import QuerySet

# Alliance Auth
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Intel Tool
from aa_intel_tool import __title__

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def _create_alliance(alliance_ids: Iterable[int] = None) -> None:
    """
    Bulk creation of EveAllianceInfo objects

    :param alliance_ids:
    :type alliance_ids:
    :return:
    :rtype:
    """

    alliance_ids = set(alliance_ids)

    existing_alliance_ids = set(
        EveAllianceInfo.objects.filter(alliance_id__in=alliance_ids).values_list(
            "alliance_id", flat=True
        )
    )

    alliances_to_fetch = alliance_ids - existing_alliance_ids
    count_alliances_to_fetch = len(alliances_to_fetch)

    if alliances_to_fetch:
        logger.debug(
            f"{count_alliances_to_fetch} EveAllianceInfo object(s) need to be created …"
        )

        for loop_count, alliance_id in enumerate(alliances_to_fetch):
            alliance = EveAllianceInfo.objects.create_alliance(alliance_id=alliance_id)

            logger.debug(
                f"({loop_count + 1}/{count_alliances_to_fetch}) "
                f"EveAllianceInfo object created for: {alliance.alliance_name}"
            )


def _create_corporation(corporation_ids: Iterable[int] = None) -> None:
    """
    Bulk creation of EveCorporationInfo objects

    :param corporation_ids:
    :type corporation_ids:
    :return:
    :rtype:
    """

    corporation_ids = set(corporation_ids)

    existing_corporation_ids = set(
        EveCorporationInfo.objects.filter(
            corporation_id__in=corporation_ids
        ).values_list("corporation_id", flat=True)
    )

    corporations_to_fetch = corporation_ids - existing_corporation_ids
    count_corporations_to_fetch = len(corporations_to_fetch)

    if corporations_to_fetch:
        logger.debug(
            f"{count_corporations_to_fetch} EveCorporationInfo object(s) need to be created …"  # pylint: disable=line-too-long
        )

        for loop_count, corporation_id in enumerate(corporations_to_fetch):
            corporation = EveCorporationInfo.objects.create_corporation(
                corp_id=corporation_id
            )

            logger.debug(
                f"({loop_count + 1}/{count_corporations_to_fetch}) "
                f"EveCorporationInfo object created for: {corporation.corporation_name}"
            )


def _create_character(
    character_ids: Iterable[int] = None, with_affiliation: bool = True
) -> None:
    """
    Bulk creation of EveCharacter objects

    :param character_ids:
    :type character_ids:
    :param with_affiliation:
    :type with_affiliation:
    :return:
    :rtype:
    """

    character_ids = set(character_ids)

    count_characters_to_fetch = len(character_ids)

    logger.debug(
        f"{count_characters_to_fetch} EveCharacter object(s) need to be created …"
    )

    tmp_character_ids = {"corporation": [], "alliance": []}

    for loop_count, character_id in enumerate(character_ids):
        # Create character
        character = EveCharacter.objects.create_character(character_id=character_id)

        logger.debug(
            f"({loop_count + 1}/{count_characters_to_fetch}) "
            f"EveCharacter object created for: {character.character_name}"
        )

        if character.alliance_id is not None:
            tmp_character_ids["alliance"].append(character.alliance_id)
        else:
            tmp_character_ids["corporation"].append(character.corporation_id)

    if with_affiliation is True:
        if len(tmp_character_ids["alliance"]) > 0:
            _create_alliance(tmp_character_ids["alliance"])

        if len(tmp_character_ids["corporation"]) > 0:
            _create_corporation(tmp_character_ids["corporation"])


def get_or_create_character(
    character_ids: Iterable[int] = None,
) -> QuerySet[EveCharacter]:
    """
    This function takes a list of character IDs and checks if the characters already
    exist in Auth and creates them with their corporation and alliance associations,
    if needed.

    :param character_ids:
    :type character_ids:
    :return:
    :rtype:
    """

    character_ids = set(character_ids)

    logger.debug(
        msg=f"Getting information for {len(character_ids)} character(s) from AA …"
    )

    existing_character_ids = set(
        EveCharacter.objects.filter(character_id__in=character_ids).values_list(
            "character_id", flat=True
        )
    )

    character_ids_to_fetch = character_ids - existing_character_ids

    if character_ids_to_fetch:
        _create_character(character_ids=character_ids_to_fetch, with_affiliation=True)

    characters = EveCharacter.objects.filter(character_id__in=character_ids)

    return characters
