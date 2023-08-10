"""
Our URL config
"""

# Django
from django.urls import include, path

# AA Intel Tool
from aa_intel_tool.constants import INTERNAL_URL_PREFIX
from aa_intel_tool.views import ajax, general

app_name: str = "aa_intel_tool"


app_urls = [
    path(route="", view=general.index, name="intel_tool_index"),
    path(route="scan/<str:scan_hash>/", view=general.scan, name="intel_tool_scan"),
]

ajax_urls = [
    path(
        route="get-scan-data/<str:scan_hash>/<str:scan_section>/",
        view=ajax.get_scan_data,
        name="ajax_get_scan_data",
    ),
]

# Put it all together
urlpatterns = [
    # Ajax
    path(f"{INTERNAL_URL_PREFIX}/ajax/", include(ajax_urls)),
    # App URLs
    path("", include(app_urls)),
]
