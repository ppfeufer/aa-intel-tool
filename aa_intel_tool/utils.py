"""
utility functions
"""

# Django
from django.core.handlers.wsgi import WSGIRequest


def user_is_logged_in(request: WSGIRequest) -> bool:
    """
    check if a user is logged in
    :param request:
    :type request:
    :return:
    :rtype:
    """

    return request.user.is_authenticated


def get_template_view(request: WSGIRequest) -> str:
    """
    determine if we need "public" or "internal"
    :param request:
    :type request:
    :return:
    :rtype:
    """

    template_view = "public"
    if user_is_logged_in(request):
        template_view = "internal"

    return template_view
