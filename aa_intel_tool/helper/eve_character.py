"""
Some little helper to deal with Eve characters
"""
# Standard Library
from typing import Optional

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
from aa_intel_tool.exceptions import NoDataError
from aa_intel_tool.providers import esi

logger = LoggerAddTag(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def get_or_create_character(
    name: str = None, character_id: int = None
) -> Optional[EveCharacter]:
    """
    This function takes a name or id of a character and checks
    to see if the character already exists.
    If the character does not already exist, it will create the
    character object, and if needed the corp/alliance objects as well.

    :param name:
    :type name:
    :param character_id:
    :type character_id:
    :return:
    :rtype:
    """

    eve_character = None

    if name:
        # If a name is passed to this function, we have to check it on ESI
        result = esi.client.Universe.post_universe_ids(names=[name]).results()

        if "characters" not in result or result["characters"] is None:
            return None

        character_id = result["characters"][0]["id"]
        try:
            eve_character = EveCharacter.objects.get(character_id=character_id)
        except EveCharacter.DoesNotExist:  # pylint: disable=no-member
            eve_character = None
    elif character_id:
        # If an ID is passed to this function, we can just check the db for it.
        try:
            eve_character = EveCharacter.objects.get(character_id=character_id)
        except EveCharacter.DoesNotExist:  # pylint: disable=no-member
            eve_character = None
    elif not name and not character_id:
        raise NoDataError("No character name or character id provided.")

    if eve_character is None:
        # Create character
        character = EveCharacter.objects.create_character(character_id=character_id)

        logger.debug(f"EveCharacter Object created: {character.character_name}")

        # Create alliance and corporation info objects if not already exists for
        # future sanity
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

        character = EveCharacter.objects.get(pk=character.pk)
    else:
        character = eve_character

    return character
