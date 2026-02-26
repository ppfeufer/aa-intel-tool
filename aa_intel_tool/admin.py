"""
Django admin integration
"""

# Django
from django.contrib import admin
from django.utils import html, safestring
from django.utils.translation import gettext_lazy as _

# AA Intel Tool
from aa_intel_tool.helper.urls import reverse_absolute
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

        :param request: The HTTP request object containing metadata about the request and user input (not used in this function but included for consistency with Django admin patterns)
        :type request: HttpRequest
        :return: False, indicating that no "add" permissions are granted for this admin model, effectively making it read-only in terms of adding new entries through the admin interface
        :rtype: bool
        """

        return False

    @staticmethod
    def has_change_permission(request, obj=None):  # pylint: disable=unused-argument
        """
        Has "change" permissions

        :param request: The HTTP request object containing metadata about the request and user input (not used in this function but included for consistency with Django admin patterns)
        :type request: HttpRequest
        :param obj: The specific object being checked for change permissions (not used in this function but included for consistency with Django admin patterns)
        :type obj: Model instance or None
        :return: False, indicating that no "change" permissions are granted for this admin model, effectively making it read-only in terms of modifying existing entries through the admin interface
        :rtype: bool
        """

        return False

    @staticmethod
    def has_delete_permission(request, obj=None):  # pylint: disable=unused-argument
        """
        Has "delete" permissions

        :param request: The HTTP request object containing metadata about the request and user input (not used in this function but included for consistency with Django admin patterns)
        :type request: HttpRequest
        :param obj: The specific object being checked for delete permissions (not used in this function but included for consistency with Django admin patterns)
        :type obj: Model instance or None
        :return: False, indicating that no "delete" permissions are granted for this admin model, effectively making it read-only in terms of deleting existing entries through the admin interface
        :rtype: bool
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

        :param obj: The Scan object being displayed in the admin interface, which contains information about the scan type and its unique hash identifier, used to generate a link to the scan's detail view in a new browser tab
        :type obj: Scan
        :return: A string containing the human-readable scan type along with an HTML link that opens the scan's detail view in a new browser tab, allowing administrators to quickly access the full details of the scan directly from the admin list view
        :rtype: str
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

        :param obj: The Scan object being displayed in the admin interface, which contains the raw data of the scan that needs to be formatted for better readability in the admin list view
        :type obj: Scan
        :return: A string containing the raw data of the scan formatted within HTML <pre> tags to preserve whitespace and formatting, making it easier for administrators to read and analyze the raw data directly from the admin list view without needing to open the scan's detail view
        :rtype: str
        """

        return html.format_html("<pre>{}</pre>", obj.raw_data)
