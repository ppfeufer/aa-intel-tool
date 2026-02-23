"""
Little helper functions to deal with Eve characters
"""

# Standard Library
from collections.abc import Iterable
from typing import Any

# Django
from django.db.models import QuerySet

# Alliance Auth
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)
from allianceauth.services.hooks import get_extension_logger

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.providers import AppLogger, ESIHandler

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)

temp_corp_data = {}
temp_alliance_data = {}


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


def _get_corporation_info_from_affiliation(
    affiliation_data: dict,
) -> EveCorporationInfo | None:
    """
    Get corporation information from affiliation data

    :param affiliation_data:
    :type affiliation_data:
    :return:
    :rtype:
    """

    corporation_id = affiliation_data.get("corporation_id")

    if corporation_id in temp_corp_data:
        return temp_corp_data[corporation_id]

    corp_info = ESIHandler.get_corporations_corporation_id(
        corporation_id=corporation_id, use_etag=False
    )
    temp_corp_data[corporation_id] = corp_info

    return corp_info


def _get_alliance_info_from_affiliation(
    affiliation_data: dict,
) -> EveAllianceInfo | None:
    """
    Get alliance information from affiliation data

    :param affiliation_data:
    :type affiliation_data:
    :return:
    :rtype:
    """

    alliance_id = affiliation_data.get("alliance_id")

    if not alliance_id:
        return None

    if alliance_id in temp_alliance_data:
        return temp_alliance_data[alliance_id]

    alliance_info = ESIHandler.get_alliances_alliance_id(
        alliance_id=alliance_id, use_etag=False
    )

    temp_alliance_data[alliance_id] = alliance_info

    return alliance_info


def _fetch_affiliations_with_retry(chunk: list[int]) -> list[dict[str, Any]]:
    """
    Fetch affiliations with retry logic for handling ESI errors

    :param chunk: List of character IDs to fetch affiliations for
    :type chunk: list[int]
    :return: List of affiliation data or empty list if all attempts fail
    :rtype: list[dict[str, Any]]
    """

    try:
        affiliations = ESIHandler.post_characters_affiliation(ids=chunk)

        logger.debug(
            f"Affiliation information for character IDs {chunk} received from ESI: {affiliations}"
        )

        return affiliations
    except Exception as exc:  # pylint: disable=broad-exception-caught
        if len(chunk) <= 1:
            # last entry failed — ignore it
            logger.warning(
                f"Ignoring character ID {chunk[0] if chunk else 'unknown'} after exception: {exc}"
            )

            return []

        mid = len(chunk) // 2
        left = _fetch_affiliations_with_retry(chunk[:mid])
        right = _fetch_affiliations_with_retry(chunk[mid:])
        results = []

        results.extend(left or [])
        results.extend(right or [])

        logger.debug(
            f"Affiliation information for character IDs {chunk} received from ESI after retry: {results}"
        )

        return results


def _fetch_ids_with_retry(chunk: list[str]) -> list[dict[str, Any]]:
    """
    Fetch IDs with retry logic for handling ESI errors

    :param chunk: List of names to fetch IDs for
    :type chunk: list[str]
    :return: List of ID data or empty list if all attempts fail
    :rtype: list[dict[str, Any]]
    """

    try:
        response = ESIHandler.post_universe_ids(names=chunk)

        logger.debug(f"ID information for names {chunk} received from ESI: {response}")

        try:
            response_as_dict = response.model_dump()
        except AttributeError:
            response_as_dict = {}

        logger.debug(f"ID information after model_dump: {response_as_dict}")

        return (
            response_as_dict["characters"] if "characters" in response_as_dict else []
        )
    except Exception as exc:  # pylint: disable=broad-exception-caught
        if len(chunk) <= 1:
            # last entry failed — ignore it
            logger.warning(
                f"Ignoring name {chunk[0] if chunk else 'unknown'} after exception: {exc}"
            )

            return []

        mid = len(chunk) // 2

        # Recursively fetch left half of the chunk, and handle potential AttributeError when calling model_dump()
        left = _fetch_ids_with_retry(chunk[:mid])
        try:
            left_as_dict = left.model_dump()
        except AttributeError:
            left_as_dict = {}

        # Recursively fetch right half of the chunk, and handle potential AttributeError when calling model_dump()
        right = _fetch_ids_with_retry(chunk[mid:])
        try:
            right_as_dict = right.model_dump()
        except AttributeError:
            right_as_dict = {}

        results = []

        # Extract "characters" from left response if available, and handle cases where model_dump() might not return a dict
        results.extend(left_as_dict.get("characters", []))

        # Extract "characters" from right response if available, and handle cases where model_dump() might not return a dict
        results.extend(right_as_dict.get("characters", []))

        logger.debug(
            f"ID information for names received from ESI after retry: {results}"
        )

        return results


def create_characters(  # pylint: disable=too-many-locals
    character_data_from_esi: list[dict[str, Any]], with_affiliation: bool = True
) -> QuerySet[EveCharacter]:
    """
    Bulk creation of EveCharacter objects

    :param character_data_from_esi:
    :type character_data_from_esi:
    :param with_affiliation:
    :type with_affiliation:
    :return:
    :rtype:
    """

    logger.debug(
        f"Character list: {character_data_from_esi} (#{len(character_data_from_esi)} characters) received for creation."
    )

    affiliations = []
    affiliation_ids = {"alliances": set(), "corporations": set()}
    characters_to_create = []
    chunk_size = 1000  # ESI affiliation endpoint accepts up to 1000 IDs per request

    # Materialize input iterable so names remain available and build id->name map
    character_ids_list = [c["id"] for c in character_data_from_esi]
    id_to_name = {c["id"]: c["name"] for c in character_data_from_esi}

    for loop_count, chunk in enumerate(
        [
            list(character_ids_list)[i : i + chunk_size]
            for i in range(0, len(character_ids_list), chunk_size)
        ],
        start=1,
    ):
        logger.debug(f"Processing chunk {loop_count} with {len(chunk)} character(s) …")

        esi_response = _fetch_affiliations_with_retry(chunk=chunk)

        logger.debug(
            f"Affiliation information for chunk {loop_count} received from ESI: {esi_response}"
        )

        # Attach name from the original input when character_id matches
        affiliations.extend(
            [
                {
                    "character_id": item.character_id,
                    "character_name": id_to_name.get(item.character_id),
                    "corporation_id": getattr(item, "corporation_id", None),
                    "alliance_id": getattr(item, "alliance_id", None),
                    "faction_id": getattr(item, "faction_id", None),
                }
                for item in esi_response
            ]
        )

    logger.debug(
        f"Affiliation information received from ESI: {affiliations} (#{len(affiliations)} affiliations)"
    )

    logger.info(
        f"{len(character_ids_list)} EveCharacter object(s) need to be created …"
    )

    factions_response = ESIHandler.get_universe_factions(use_etag=False)
    faction_id_to_name = {f.faction_id: f.name for f in factions_response}

    for affiliation in affiliations:
        logger.debug(
            f"Processing affiliation for character ID {affiliation['character_id']}: {affiliation}"
        )

        corp_info = _get_corporation_info_from_affiliation(affiliation_data=affiliation)
        alliance_info = _get_alliance_info_from_affiliation(
            affiliation_data=affiliation
        )

        characters_to_create.append(
            EveCharacter(
                character_id=affiliation["character_id"],
                character_name=affiliation["character_name"],
                corporation_id=affiliation["corporation_id"],
                corporation_name=corp_info.name if corp_info else None,
                corporation_ticker=corp_info.ticker if corp_info else None,
                alliance_id=affiliation["alliance_id"],
                alliance_name=alliance_info.name if alliance_info else None,
                alliance_ticker=alliance_info.ticker if alliance_info else None,
                faction_id=(
                    affiliation["faction_id"] if affiliation["faction_id"] else None
                ),
                faction_name=(
                    faction_id_to_name.get(affiliation["faction_id"])
                    if affiliation["faction_id"]
                    else None
                ),
            )
        )

        affiliation_key = "alliances" if affiliation["alliance_id"] else "corporations"
        affiliation_ids[affiliation_key].add(
            affiliation["alliance_id"] or affiliation["corporation_id"]
        )

    logger.debug(
        f"Prepared {len(characters_to_create)} Character objects for bulk creation."
    )
    logger.debug(f"Entities to be created: {affiliation_ids}")

    # Only perform bulk_create when we actually have objects to create.
    if characters_to_create:
        logger.debug(
            f"Character objects to bulk create: count={len(characters_to_create)}; "
            f"Example: {[c.character_name for c in characters_to_create[:10]]}"
        )

        chunk_size = 500
        total_chunks = (len(characters_to_create) + chunk_size - 1) // chunk_size
        for idx in range(0, len(characters_to_create), chunk_size):
            chunk = characters_to_create[idx : idx + chunk_size]
            EveCharacter.objects.bulk_create(chunk)

            logger.debug(
                "Bulk created %d Character objects (chunk %d/%d).",
                len(chunk),
                idx // chunk_size + 1,
                total_chunks,
            )
    else:
        logger.debug("No Character objects to bulk create; skipping bulk_create.")

    if with_affiliation:
        if affiliation_ids["alliances"]:
            _create_alliance(affiliation_ids["alliances"])

        if affiliation_ids["corporations"]:
            _create_corporation(affiliation_ids["corporations"])

    return EveCharacter.objects.filter(character_id__in=character_ids_list)


def fetch_character_ids_from_esi(characters_to_fetch: set[Any]) -> list:
    """
    Fetch character IDs from ESI

    :param characters_to_fetch: Set of character IDs to fetch from ESI
    :type characters_to_fetch: set[Any]
    :return: List of character IDs fetched from ESI or None if no characters were fetched
    :rtype: list
    """

    chunk_size = 500
    fetched_characters = []

    for loop_count, chunk in enumerate(
        [
            list(characters_to_fetch)[i : i + chunk_size]
            for i in range(0, len(characters_to_fetch), chunk_size)
        ],
        start=1,
    ):
        logger.debug(
            f"Processing chunk {loop_count} with {len(chunk)} character(s): {chunk}"
        )

        esi_response = _fetch_ids_with_retry(chunk=chunk)

        logger.debug(
            f"ID information for chunk {loop_count} received from ESI: {esi_response}"
        )

        if esi_response:
            fetched_characters += esi_response

            logger.debug(
                f"ID information for chunk {loop_count} successfully processed: {esi_response}"
            )
        else:
            logger.warning(
                f"No ID information received from ESI for chunk {loop_count} with character IDs: {chunk}"
            )

    logger.debug(
        f"ID information for all chunks received from ESI: {fetched_characters} (#{len(fetched_characters)} characters)"
    )

    return fetched_characters
