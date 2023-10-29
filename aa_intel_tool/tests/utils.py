"""
Helper for our tests
"""

# Standard Library
from pathlib import Path

# Django
from django.core.handlers.wsgi import WSGIRequest
from django.template import Context, Template


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
