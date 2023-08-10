"""
App init
"""

# Standard Library
from importlib import metadata

__version__ = metadata.version(distribution_name="aa-intel-tool")
__title__ = "Intel Tool"

del metadata
