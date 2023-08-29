"""
Test auth_hooks
"""

# Standard Library
from http import HTTPStatus

# Django
from django.test import TestCase
from django.urls import reverse

# Alliance Auth (External Libs)
from app_utils.testing import create_fake_user


class TestAccess(TestCase):
    """
    Test access
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

        cls.html_menu = f"""
            <li>
                <a class="active" href="{reverse('aa_intel_tool:intel_tool_index')}">
                    <i class="fas fa-clipboard-list fa-fw"></i>
                    Intel Parser
                </a>
            </li>
        """

        cls.header = """
            <div class="aa-intel-tool-header">
                <header>
                    <h1>Intel Parser</h1>
                </header>
                <p>
                    Please keep in mind, parsing large amounts of data can take some time. Be patient, CCP's API is not the fastest to answer …
                </p>
            </div>
        """

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
        self.assertContains(response=response, text=self.html_menu, html=True)
        self.assertContains(response=response, text=self.header, html=True)

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
        self.assertContains(response=response, text=self.header, html=True)
