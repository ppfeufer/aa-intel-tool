"""
Little helper functions to deal with Eve characters
"""

# Standard Library
from typing import Iterable

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

    logger.debug(msg=f"Getting information for {len(character_ids)} characters.")

    existing_character_ids = set(
        EveCharacter.objects.filter(character_id__in=character_ids).values_list(
            "character_id", flat=True
        )
    )
    character_ids_to_fetch = character_ids - existing_character_ids

    if character_ids_to_fetch:
        count_characters_to_fetch = len(character_ids_to_fetch)

        logger.debug(
            f"{count_characters_to_fetch} EveCharacter Objects need to be created."
        )

        for loop_count, character_id in enumerate(character_ids_to_fetch):
            # Create character
            character = EveCharacter.objects.create_character(character_id=character_id)

            logger.debug(
                f"({loop_count + 1}/{count_characters_to_fetch}) "
                f"EveCharacter Object created for: {character.character_name}"
            )

            if character.alliance_id is not None:
                # Create alliance and corporation info objects if not already exists
                if not EveAllianceInfo.objects.filter(
                    alliance_id=character.alliance_id
                ).exists():
                    EveAllianceInfo.objects.create_alliance(
                        alliance_id=character.alliance_id
                    )
            else:
                # Create the corporation info object if not already exists
                if not EveCorporationInfo.objects.filter(
                    corporation_id=character.corporation_id
                ).exists():
                    EveCorporationInfo.objects.create_corporation(
                        corp_id=character.corporation_id
                    )

    characters = EveCharacter.objects.filter(character_id__in=character_ids)

    return characters
