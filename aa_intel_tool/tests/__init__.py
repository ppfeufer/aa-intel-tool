"""
Initialize the tests
"""

# Standard Library
import socket

# Django
from django.test import TestCase

# AA Intel Tool
from aa_intel_tool.tests.utils import create_fake_user


class SocketAccessError(Exception):
    """Error raised when a test script accesses the network"""


class BaseTestCase(TestCase):
    """Variation of Django's TestCase class that prevents any network use.

    Example:

        .. code-block:: python

            class TestMyStuff(BaseTestCase):
                def test_should_do_what_i_need(self): ...

    """

    @classmethod
    def setUpClass(cls):
        cls.socket_original = socket.socket
        socket.socket = cls.guard
        return super().setUpClass()

    def setUp(self):
        """
        Set up test users

        :return:
        :rtype:
        """

        super().setUp()

        self.user_1001 = create_fake_user(
            character_id=10001, character_name="Wesley Crusher"
        )

    @classmethod
    def tearDownClass(cls):
        socket.socket = cls.socket_original
        return super().tearDownClass()

    @staticmethod
    def guard(*args, **kwargs):
        raise SocketAccessError("Attempted to access network")
