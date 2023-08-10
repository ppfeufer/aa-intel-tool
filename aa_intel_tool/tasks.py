"""
The tasks
"""

# Standard Library
from datetime import timedelta

# Third Party
from celery import shared_task

# Django
from django.utils import timezone

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Intel Tool
from aa_intel_tool import __title__
from aa_intel_tool.app_settings import AppSettings
from aa_intel_tool.models import Scan

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@shared_task
def housekeeping() -> None:
    """
    Remove scans older than AppSettings.INTELTOOL_SCAN_RETENTION_TIME day(s)

    :return:
    :rtype:
    """

    if AppSettings.INTELTOOL_SCAN_RETENTION_TIME > 0:
        logger.info(
            msg=f"Removing scans older than {AppSettings.INTELTOOL_SCAN_RETENTION_TIME} day(s)"  # pylint: disable=line-too-long
        )

        Scan.objects.filter(  # pylint: disable=no-member
            created__lte=timezone.now()
            - timedelta(days=AppSettings.INTELTOOL_SCAN_RETENTION_TIME)
        ).delete()
