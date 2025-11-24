"""
Helper for our tests
"""

# Standard Library
import re
from pathlib import Path

# Django
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.template import Context, Template

# Alliance Auth
from allianceauth.tests.auth_utils import AuthUtils


def render_template(string, context=None):
    """
    Helper to render templates
    :param string:
    :param context:
    :return:
    """

    context = context or {}
    context = Context(dict_=context)

    return Template(template_string=string).render(context=context)


def load_chatscan_txt() -> str:
    """
    Loading chatscan.txt

    :return:
    :rtype:
    """

    return (Path(__file__).parent / "test-data/chatscan.txt").read_text()


def load_chatscan_faulty_txt() -> str:
    """
    Loading chatscan-faulty.txt

    :return:
    :rtype:
    """

    return (Path(__file__).parent / "test-data/chatscan-faulty.txt").read_text()


def load_dscan_txt() -> str:
    """
    Loading dscan.txt

    :return:
    :rtype:
    """

    return (Path(__file__).parent / "test-data/dscan.txt").read_text()


def load_fleetcomp_txt() -> str:
    """
    Loading fleetcomp.txt

    :return:
    :rtype:
    """

    return (Path(__file__).parent / "test-data/fleetcomp.txt").read_text()


def response_content_to_str(response: WSGIRequest) -> str:
    """
    Return the content of a WSGIRequest response as string

    :param response:
    :type response:
    :return:
    :rtype:
    """

    return response.content.decode(response.charset)


def create_fake_user(
    character_id: int,
    character_name: str,
    corporation_id: int = None,
    corporation_name: str = None,
    corporation_ticker: str = None,
    permissions: list[str] = None,
    **kwargs,
) -> User:
    """
    Create a fake user with a given character name and id.

    :param character_id:
    :type character_id:
    :param character_name:
    :type character_name:
    :param corporation_id:
    :type corporation_id:
    :param corporation_name:
    :type corporation_name:
    :param corporation_ticker:
    :type corporation_ticker:
    :param permissions:
    :type permissions:
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """

    username = re.sub(pattern=r"[^\w\d@\.\+-]", repl="_", string=character_name)
    user = AuthUtils.create_user(username=username)

    if not corporation_id:
        corporation_id = 2001
        corporation_name = "Wayne Technologies Inc."
        corporation_ticker = "WTE"

    alliance_id = kwargs.get("alliance_id", 3001)
    alliance_name = (
        kwargs.get("alliance_name", "Wayne Enterprises")
        if alliance_id is not None
        else ""
    )

    AuthUtils.add_main_character_2(
        user=user,
        name=character_name,
        character_id=character_id,
        corp_id=corporation_id,
        corp_name=corporation_name,
        corp_ticker=corporation_ticker,
        alliance_id=alliance_id,
        alliance_name=alliance_name,
    )

    if permissions:
        perm_objs = [AuthUtils.get_permission_by_name(perm) for perm in permissions]
        user = AuthUtils.add_permissions_to_user(perms=perm_objs, user=user)

    return user
