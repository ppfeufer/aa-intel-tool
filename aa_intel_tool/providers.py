"""
Providers for the AA Intel Tool app.
"""

# Standard Library
import logging
from typing import Any

# Third Party
from aiopenapi3 import ContentTypeError
from httpx import Response

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from esi.exceptions import HTTPClientError, HTTPNotModified
from esi.openapi_clients import ESIClientProvider, EsiOperation

# AA Intel Tool
from aa_intel_tool import (
    __app_name_verbose__,
    __esi_compatibility_date__,
    __github_url__,
    __title__,
    __version__,
)

# ESI client
esi = ESIClientProvider(
    # ESI compatibility date, see https://esi.evetech.net/meta/compatibility-dates
    compatibility_date=__esi_compatibility_date__,
    # User agent for the ESI client
    ua_appname=__app_name_verbose__,
    ua_version=__version__,
    ua_url=__github_url__,
    operations=[
        "GetAlliancesAllianceId",
        "GetCorporationsCorporationId",
        "GetUniverseFactions",
        "PostCharactersAffiliation",
        "PostUniverseIds",
    ],
)


class ESIHandler:
    """
    Handler for ESI operations, providing a method to retrieve results while handling exceptions.
    """

    @classmethod
    def result(  # pylint: disable=too-many-arguments, too-many-positional-arguments
        cls,
        operation: EsiOperation,
        use_etag: bool = True,
        return_response: bool = False,
        force_refresh: bool = False,
        use_cache: bool = True,
        **extra,
    ) -> tuple[Any, Response] | Any:
        """
        Retrieve the result of an ESI operation, handling HTTPNotModified exceptions.

        :param operation: The ESI operation to execute.
        :type operation: EsiOperation
        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :param return_response: Whether to return the full response object.
        :type return_response: bool
        :param force_refresh: Whether to force a refresh of the data.
        :type force_refresh: bool
        :param use_cache: Whether to use cached data.
        :type use_cache: bool
        :param extra: Additional parameters to pass to the operation.
        :type extra: dict
        :return: The result of the ESI operation, optionally with the response object.
        :rtype: tuple[Any, Response] | Any
        """

        logger.debug(f"Handling ESI operation: {operation.operation.operationId}")

        try:
            esi_result = operation.result(
                use_etag=use_etag,
                return_response=return_response,
                force_refresh=force_refresh,
                use_cache=use_cache,
                **extra,
            )
        except HTTPNotModified:
            logger.debug(
                f"ESI returned 304 Not Modified for operation: {operation.operation.operationId} - Skipping update."
            )

            esi_result = None
        except ContentTypeError:
            logger.warning(
                msg="ESI returned gibberish (ContentTypeError) - Skipping update."
            )

            esi_result = None
        except HTTPClientError as exc:
            logger.error(msg=f"Error while fetching data from ESI: {str(exc)}")

            esi_result = None

        return esi_result

    @classmethod
    def get_alliances_alliance_id(
        cls, alliance_id: int, use_etag: bool = True
    ) -> dict[str, Any] | None:
        """
        Get information about an alliance by its ID.

        :param alliance_id: The ID of the alliance to retrieve information for.
        :type alliance_id: int
        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :return: Alliance information as a dictionary, or None if an error occurs.
        :rtype: dict[str, Any] | None
        """

        logger.debug(f"Getting alliance information for alliance ID: {alliance_id}")

        return cls.result(
            operation=esi.client.Alliance.GetAlliancesAllianceId(
                alliance_id=alliance_id
            ),
            use_etag=use_etag,
        )

    @classmethod
    def get_corporations_corporation_id(
        cls, corporation_id: int, use_etag: bool = True
    ) -> dict[str, Any] | None:
        """
        Get information about a corporation by its ID.

        :param corporation_id: The ID of the corporation to retrieve information for.
        :type corporation_id: int
        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :return: Corporation information as a dictionary, or None if an error occurs.
        :rtype: dict[str, Any] | None
        """

        logger.debug(
            f"Getting corporation information for corporation ID: {corporation_id}"
        )

        return cls.result(
            operation=esi.client.Corporation.GetCorporationsCorporationId(
                corporation_id=corporation_id
            ),
            use_etag=use_etag,
        )

    @classmethod
    def get_universe_factions(
        cls, use_etag: bool = True
    ) -> list[dict[str, Any]] | None:
        """
        Get a list of factions.

        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :return: List of faction data or None if an error occurs.
        :rtype: list[dict[str, Any]] | None
        """

        logger.debug("Getting factions")

        return cls.result(
            operation=esi.client.Universe.GetUniverseFactions(), use_etag=use_etag
        )

    @classmethod
    def post_characters_affiliation(cls, ids: list[int]) -> list[dict[str, Any]] | None:
        """
        Get affiliations for a list of IDs.

        :param ids: List of character, corporation, or alliance IDs.
        :type ids: list[int]
        :return: List of affiliation data or None if an error occurs.
        :rtype: list[dict[str, Any]] | None
        """

        logger.debug(f"Getting affiliations for IDs: {ids}")

        return cls.result(
            operation=esi.client.Character.PostCharactersAffiliation(body=ids)
        )

    @classmethod
    def post_universe_ids(cls, names: list[str]) -> list[dict[str, Any]] | None:
        """
        Get IDs for a list of names.

        :param names: List of character, corporation, alliance, or faction names.
        :type names: list[str]
        :return: List of ID data or None if an error occurs.
        :rtype: list[dict[str, Any]] | None
        """

        logger.debug(f"Getting IDs for names: {names}")

        return cls.result(operation=esi.client.Universe.PostUniverseIds(body=names))


class AppLogger(logging.LoggerAdapter):
    """
    Custom logger adapter that adds a prefix to log messages.

    Taken from the `allianceauth-app-utils` package.
    Credits to: Erik Kalkoken
    """

    def __init__(self, my_logger, prefix):
        """
        Initializes the AppLogger with a logger and a prefix.

        :param my_logger: Logger instance
        :type my_logger: logging.Logger
        :param prefix: Prefix string to add to log messages
        :type prefix: str
        """

        super().__init__(my_logger, {})

        self.prefix = prefix

    def process(self, msg, kwargs):
        """
        Prepares the log message by adding the prefix.

        :param msg: Log message
        :type msg: str
        :param kwargs: Additional keyword arguments
        :type kwargs: dict
        :return: Prefixed log message and kwargs
        :rtype: tuple
        """

        return f"[{self.prefix}] {msg}", kwargs


logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)
