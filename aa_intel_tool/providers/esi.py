"""
Providers for the AA Intel Tool app.
"""

# Standard Library
from typing import Any

# Third Party
from aiopenapi3 import ContentTypeError, RequestError
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
    __version__,
)
from aa_intel_tool.providers.applogger import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__))

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
    ) -> Any | tuple[Any, Response] | None:
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
        :return: The result of the ESI operation.
        :rtype: Any | tuple[Any, Response] | None
        """

        logger.debug(f"Handling ESI operation: {operation.operation.operationId}")
        logger.debug(
            f"Operation parameters: use_etag={use_etag}, return_response={return_response}, force_refresh={force_refresh}, use_cache={use_cache}, extra={extra}"
        )

        response: Response | None = None

        try:
            # Call operation.result differently depending on whether the caller
            # requested the raw Response object. Some implementations return a
            # single result when return_response is False and a (result, response)
            # tuple when True, so only unpack when return_response is True.
            if return_response:
                esi_result, response = operation.result(
                    use_etag=use_etag,
                    return_response=return_response,
                    force_refresh=force_refresh,
                    use_cache=use_cache,
                    **extra,
                )

                logger.debug(
                    f"ESI Response for operation: {operation.operation.operationId}: {response}"
                )
            else:
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
        except (HTTPClientError, RequestError) as exc:
            logger.error(msg=f"Error while fetching data from ESI: {str(exc)}")

            esi_result = None

        # If caller requested the raw response, return a tuple (result, response)
        if return_response:
            return esi_result, response

        return esi_result

    @classmethod
    def get_alliances_alliance_id(
        cls, alliance_id: int, use_etag: bool = True
    ) -> tuple[Any, Response] | None | Any:
        """
        Get information about an alliance by its ID.

        :param alliance_id: The ID of the alliance to retrieve information for.
        :type alliance_id: int
        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :return: Alliance information as a dictionary, or None if an error occurs.
        :rtype: tuple[Any, Response] | None | Any
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
    ) -> tuple[Any, Response] | None | Any:
        """
        Get information about a corporation by its ID.

        :param corporation_id: The ID of the corporation to retrieve information for.
        :type corporation_id: int
        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :return: Corporation information as a dictionary, or None if an error occurs.
        :rtype: tuple[Any, Response] | None | Any
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
    ) -> tuple[Any, Response] | None | Any:
        """
        Get a list of factions.

        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :return: List of faction data or None if an error occurs.
        :rtype: tuple[Any, Response] | None | Any
        """

        logger.debug("Getting factions")

        return cls.result(
            operation=esi.client.Universe.GetUniverseFactions(), use_etag=use_etag
        )

    @classmethod
    def post_characters_affiliation(
        cls, ids: list[int]
    ) -> tuple[Any, Response] | None | Any:
        """
        Get affiliations for a list of IDs.

        :param ids: List of character, corporation, or alliance IDs.
        :type ids: list[int]
        :return: List of affiliation data or None if an error occurs.
        :rtype: tuple[Any, Response] | None | Any
        """

        logger.debug(f"Getting affiliations for IDs: {ids}")

        return cls.result(
            operation=esi.client.Character.PostCharactersAffiliation(body=ids)
        )

    @classmethod
    def post_universe_ids(cls, names: list[str]) -> tuple[Any, Response] | None | Any:
        """
        Get IDs for a list of names.

        :param names: List of character, corporation, alliance, or faction names.
        :type names: list[str]
        :return: List of ID data or None if an error occurs.
        :rtype: tuple[Any, Response] | None | Any
        """

        logger.debug(f"Getting IDs for names: {names}")

        return cls.result(operation=esi.client.Universe.PostUniverseIds(body=names))
