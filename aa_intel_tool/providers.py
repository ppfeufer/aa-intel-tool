"""
Providers
"""

# Alliance Auth
from esi.clients import EsiClientProvider

# AA Intel Tool
from aa_intel_tool.constants import USER_AGENT

esi = EsiClientProvider(app_info_text=USER_AGENT)
