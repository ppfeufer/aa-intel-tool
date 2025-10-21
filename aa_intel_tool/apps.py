"""
App config
"""

# Django
from django.apps import AppConfig
from django.utils.text import format_lazy

# AA Intel Tool
from aa_intel_tool import __title_translated__, __version__


class AaIntelToolConfig(AppConfig):
    """
    Application config
    """

    name = "aa_intel_tool"
    label = "aa_intel_tool"
    verbose_name = format_lazy(
        "{app_title} v{version}", app_title=__title_translated__, version=__version__
    )
