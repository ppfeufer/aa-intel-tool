"""
URL helper functions for AA Forum.
"""

# Standard Library
from urllib.parse import urljoin

# Django
from django.conf import settings
from django.urls import reverse


def reverse_absolute(viewname: str, args: list | None = None) -> str:
    """
    Reverse a view name to an absolute URL.

    :param viewname: The name of the view to reverse.
    :type viewname: str
    :param args:
    :type args: list | None
    :return: Absolute URL for the given view name and arguments.
    :rtype: str
    """

    return urljoin(base=settings.SITE_URL, url=reverse(viewname=viewname, args=args))
