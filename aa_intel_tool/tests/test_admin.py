"""
Test for admin.py
"""

# Django
from django.test import TestCase
from django.urls import reverse

# Alliance Auth (External Libs)
from app_utils.testing import create_fake_user

# AA Intel Tool
from aa_intel_tool.admin import BaseReadOnlyAdminMixin


class TestAdmin(TestCase):
    """
    The tests
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        # User
        cls.user_1001 = create_fake_user(
            character_id=1001, character_name="Peter Parker"
        )

    def test_has_add_permission_returns_false(self):
        """
        Test if admin.BaseReadOnlyAdminMixin.has_add_permission returns False

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_1001)

        response = self.client.get(
            path=reverse(viewname="aa_intel_tool:intel_tool_index")
        )

        has_permission = BaseReadOnlyAdminMixin.has_add_permission(request=response)

        self.assertFalse(expr=has_permission)

    def test_has_change_permission_returns_false(self):
        """
        Test if admin.BaseReadOnlyAdminMixin.has_change_permission returns False

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_1001)

        response = self.client.get(
            path=reverse(viewname="aa_intel_tool:intel_tool_index")
        )

        has_permission = BaseReadOnlyAdminMixin.has_change_permission(request=response)

        self.assertFalse(expr=has_permission)

    def test_has_delete_permission_returns_false(self):
        """
        Test if admin.BaseReadOnlyAdminMixin.has_delete_permission returns False

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_1001)

        response = self.client.get(
            path=reverse(viewname="aa_intel_tool:intel_tool_index")
        )

        has_permission = BaseReadOnlyAdminMixin.has_delete_permission(request=response)

        self.assertFalse(expr=has_permission)
