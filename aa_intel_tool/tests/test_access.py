"""
Test auth_hooks
"""

# Standard Library
from http import HTTPStatus

# Django
from django.urls import reverse

# AA Intel Tool
from aa_intel_tool.tests import BaseTestCase
from aa_intel_tool.tests.utils import response_content_to_str


class TestAccess(BaseTestCase):
    """
    Test access
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.html_menu = f"""
            <li class="d-flex flex-wrap m-2 p-2 pt-0 pb-0 mt-0 mb-0 me-0 pe-0">
                <i class="nav-link fa-solid fa-clipboard-list fa-fw align-self-center me-3 active"></i>
                <a class="nav-link flex-fill align-self-center me-auto active" href="{reverse('aa_intel_tool:intel_tool_index')}">
                    Intel Parser
                </a>
            </li>
        """

        cls.header_top = '<div class="navbar-brand">Intel Parser</div>'

        cls.header_public_page = '<div class="navbar-brand">Intel Parser</div>'

    def test_access_to_index_for_logged_in_user(self):
        """
        Test should open the index view for logged-in user

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_1001)

        response = self.client.get(
            path=reverse(viewname="aa_intel_tool:intel_tool_index")
        )

        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        # self.assertContains(response=response, text=self.html_menu, html=True)
        # self.assertContains(response=response, text=self.header_top, html=True)
        self.assertInHTML(
            needle=self.html_menu, haystack=response_content_to_str(response)
        )
        self.assertInHTML(
            needle=self.header_top, haystack=response_content_to_str(response)
        )

    def test_access_to_index_as_public_page(self):
        """
        Test should open the index view as public page

        :return:
        :rtype:
        """

        response = self.client.get(
            path=reverse(viewname="aa_intel_tool:intel_tool_index")
        )

        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        # self.assertContains(response=response, text=self.header_public_page, html=True)
        self.assertInHTML(
            needle=self.header_public_page, haystack=response_content_to_str(response)
        )
