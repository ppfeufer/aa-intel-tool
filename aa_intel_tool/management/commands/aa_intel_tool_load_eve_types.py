"""
Preloads data required for AA Intel Tool from ESI
"""

# Standard Library
import logging

# Django
from django.core.management import call_command
from django.core.management.base import BaseCommand

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from eveuniverse.constants import EveCategoryId

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.app_settings import AdditionalEveCategoryId

logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class Command(BaseCommand):
    """
    Pre-loading required data
    """

    help = "Preloads data required for AA Intel Tool from ESI"

    def add_arguments(self, parser):
        """
        Adding arguments to the command parser

        :param parser:
        :type parser:
        :return:
        :rtype:
        """

        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_true",
            help="Do NOT prompt the user for input of any kind.",
        )

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """
        Start the eve type import

        :param args:
        :type args:
        :param options:
        :type options:
        :return:
        :rtype:
        """

        params = [
            "eveuniverse_load_types",
            __title__,
            "--category_id",
            str(EveCategoryId.SHIP.value),
            "--category_id",
            str(EveCategoryId.STRUCTURE.value),
            "--category_id",
            str(AdditionalEveCategoryId.DEPLOYABLE.value),
            "--category_id",
            str(AdditionalEveCategoryId.STARBASE.value),
        ]

        if options["noinput"]:
            params.append("--noinput")

        call_command(*params)
