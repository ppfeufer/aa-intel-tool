"""
App init
"""

# Standard Library
from importlib import metadata

# Django
from django.utils.translation import gettext_lazy as _

__version__ = metadata.version(distribution_name="aa-intel-tool")
__title__ = _("Intel Parser")

del metadata
