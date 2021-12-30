"""
app config
"""

# Django
from django.apps import AppConfig

# AA Intel Tool
from aa_intel_tool import __version__


class AaIntelToolConfig(AppConfig):
    """
    application config
    """

    name = "aa_intel_tool"
    label = "aa_intel_tool"
    verbose_name = f"Intel Tool v{__version__}"
