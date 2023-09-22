"""
Django admin integration
"""

# Django
from django.contrib import admin
from django.utils import html, safestring
from django.utils.translation import gettext_lazy as _

# Alliance Auth (External Libs)
from app_utils.urls import reverse_absolute

# AA Intel Tool
from aa_intel_tool.models import Scan


class BaseReadOnlyAdminMixin:
    """
    Base "Read Only" mixin for admin models
    """

    actions = None  # Removes the default delete action.

    @staticmethod
    def has_add_permission(request):  # pylint: disable=unused-argument
        """
        Has "add" permissions

        :param request:
        :type request:
        :return:
        :rtype:
        """

        return False

    @staticmethod
    def has_change_permission(request, obj=None):  # pylint: disable=unused-argument
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

    @staticmethod
    def has_delete_permission(request, obj=None):  # pylint: disable=unused-argument
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

    list_display = ("hash", "scan_type", "created")
    fields = ("_scan_type", "_raw_data")

    ordering = ("-created",)

    @admin.display(description=_("Scan type"))
    def _scan_type(self, obj) -> str:
        """
        Add link to open the scan in a new browser tab

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        intel_type = obj.get_scan_type_display()
        scan_link = reverse_absolute(
            viewname="aa_intel_tool:intel_tool_scan", args=[obj.hash]
        )
        link_text = _("Open in a new browser tab")

        return safestring.mark_safe(
            f'{intel_type} (<a href="{scan_link}" target="_blank" rel="noreferer noopener">{link_text}</a>)'
        )

    @admin.display(description=_("Raw data"))
    def _raw_data(self, obj) -> str:
        """
        Format the output properly

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return html.format_html("<pre>{}</pre>", obj.raw_data)
