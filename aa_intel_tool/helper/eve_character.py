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


def _create_alliance(alliance_ids: Iterable[int]) -> None:
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

    if alliances_to_fetch:
        logger.debug(
            f"{len(alliances_to_fetch)} EveAllianceInfo object(s) need to be created …"
        )

        for loop_count, alliance_id in enumerate(alliances_to_fetch, start=1):
            alliance = EveAllianceInfo.objects.create_alliance(alliance_id=alliance_id)
            logger.debug(
                f"({loop_count}/{len(alliances_to_fetch)}) "
                f"EveAllianceInfo object created for: {alliance.alliance_name}"
            )


def _create_corporation(corporation_ids: Iterable[int]) -> None:
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

    if corporations_to_fetch:
        logger.debug(
            f"{len(corporations_to_fetch)} EveCorporationInfo object(s) need to be created …"
        )

        for loop_count, corporation_id in enumerate(corporations_to_fetch, start=1):
            corporation = EveCorporationInfo.objects.create_corporation(
                corp_id=corporation_id
            )

            logger.debug(
                f"({loop_count}/{len(corporations_to_fetch)}) "
                f"EveCorporationInfo object created for: {corporation.corporation_name}"
            )


def _create_character(
    character_ids: Iterable[int], with_affiliation: bool = True
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
    tmp_affiliation_ids = {"alliance": set(), "corporation": set()}

    logger.info(f"{len(character_ids)} EveCharacter object(s) need to be created …")

    for loop_count, character_id in enumerate(character_ids, start=1):
        # Create character
        character = EveCharacter.objects.create_character(character_id=character_id)

        logger.debug(
            f"({loop_count}/{len(character_ids)}) "
            f"EveCharacter object created for: {character.character_name}"
        )

        affiliation_key = "alliance" if character.alliance_id else "corporation"
        tmp_affiliation_ids[affiliation_key].add(
            character.alliance_id or character.corporation_id
        )

    if with_affiliation:
        if tmp_affiliation_ids["alliance"]:
            _create_alliance(tmp_affiliation_ids["alliance"])

        if tmp_affiliation_ids["corporation"]:
            _create_corporation(tmp_affiliation_ids["corporation"])


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

    character_ids = set(character_ids or [])

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

    return EveCharacter.objects.filter(character_id__in=character_ids)
