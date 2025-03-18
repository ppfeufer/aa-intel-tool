"""
Test for admin.py
"""

# Django
from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.urls import reverse

# AA Intel Tool
from aa_intel_tool.admin import BaseReadOnlyAdminMixin, ScanAdmin
from aa_intel_tool.models import Scan


class TestBaseReadOnlyAdminMixin(TestCase):
    """
    Test the BaseReadOnlyAdminMixin class
    """

    def test_add_permission_is_denied(self):
        """
        Test if admin.BaseReadOnlyAdminMixin.has_add_permission returns False

        :return:
        :rtype:
        """

        request = RequestFactory().get(
            path=reverse(viewname="aa_intel_tool:intel_tool_index")
        )

        self.assertFalse(BaseReadOnlyAdminMixin.has_add_permission(request))

    def test_change_permission_is_denied(self):
        """
        Test if admin.BaseReadOnlyAdminMixin.has_change_permission returns False

        :return:
        :rtype:
        """

        request = RequestFactory().get(
            path=reverse(viewname="aa_intel_tool:intel_tool_index")
        )

        self.assertFalse(BaseReadOnlyAdminMixin.has_change_permission(request))

    def test_delete_permission_is_denied(self):
        """
        Test if admin.BaseReadOnlyAdminMixin.has_delete_permission returns False

        :return:
        :rtype:
        """

        request = RequestFactory().get(
            path=reverse(viewname="aa_intel_tool:intel_tool_index")
        )

        self.assertFalse(BaseReadOnlyAdminMixin.has_delete_permission(request))


class TestScanAdmin(TestCase):
    """
    Test the ScanAdmin class
    """

    def test_displays_scan_type_with_link(self):
        """
        Test if ScanAdmin._scan_type displays the scan type with a link

        :return:
        :rtype:
        """

        scan = Scan(raw_data="test data")
        scan.save()

        admin_instance = ScanAdmin(model=Scan, admin_site=admin.site)
        result = admin_instance._scan_type(scan)

        self.assertIn("Open in a new browser tab", result)
        self.assertIn(scan.hash, result)

    def test_displays_raw_data_in_pre_tag(self):
        """
        Test if ScanAdmin._raw_data displays the raw data in a <pre> tag

        :return:
        :rtype:
        """

        scan = Scan.objects.create(raw_data="test data")

        admin_instance = ScanAdmin(model=Scan, admin_site=admin.site)
        result = admin_instance._raw_data(scan)

        self.assertIn("<pre>test data</pre>", result)
