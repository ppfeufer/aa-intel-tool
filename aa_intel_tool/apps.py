"""
App config
"""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# AA Intel Tool
from aa_intel_tool import __version__


class AaIntelToolConfig(AppConfig):
    """
    Application config
    """

    name = "aa_intel_tool"
    label = "aa_intel_tool"
    # Translators: This is the app name and version, which will appear in the Django Backend
    verbose_name = _(f"Intel Parser v{__version__}")
