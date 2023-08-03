"""
Django admin integration
"""

# Django
from django.contrib import admin

# AA Intel Tool
from aa_intel_tool.models import Scan


class BaseReadOnlyAdminMixin:
    """
    Base "Read Only" mixin for admin models
    """

    actions = None  # Removes the default delete action.

    def has_add_permission(self, request):  # pylint: disable=unused-argument
        """
        Has "add" permissions

        :param request:
        :type request:
        :return:
        :rtype:
        """

        return False

    def has_change_permission(
        self, request, obj=None  # pylint: disable=unused-argument
    ):
        """
        Has "change" permissions

        :param request:
        :type request:
        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return False

    def has_delete_permission(
        self, request, obj=None  # pylint: disable=unused-argument
    ):
        """
        Has "delete" permissions

        :param request:
        :type request:
        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return False


@admin.register(Scan)
class ScanAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    """
    Scan Admin
    """

    list_display = ("hash", "created")
