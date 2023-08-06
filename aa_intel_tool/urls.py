"""
Our URL config
"""

# Django
from django.urls import include, path, re_path

# AA Intel Tool
from aa_intel_tool.constants import INTERNAL_URL_PREFIX
from aa_intel_tool.views import ajax, general

app_name: str = "aa_intel_tool"


app_urls = [
    path(route="", view=general.index, name="intel_tool_index"),
    re_path(
        route=r"^scan/(?P<scan_hash>[a-zA-Z0-9]+)/$",
        view=general.scan,
        name="intel_tool_scan",
    ),
]

ajax_urls = [
    re_path(
        route=r"^get-pilot-list/(?P<scan_hash>[a-zA-Z0-9]+)/$",
        view=ajax.get_pilot_list,
        name="ajax_get_pilot_list",
    ),
    re_path(
        route=r"^get-corporation-list/(?P<scan_hash>[a-zA-Z0-9]+)/$",
        view=ajax.get_corporation_list,
        name="ajax_get_corporation_list",
    ),
    re_path(
        route=r"^get-alliance-list/(?P<scan_hash>[a-zA-Z0-9]+)/$",
        view=ajax.get_alliance_list,
        name="ajax_get_alliance_list",
    ),
]

# Put it all together
urlpatterns = [
    # Ajax
    path(f"{INTERNAL_URL_PREFIX}/ajax/", include(ajax_urls)),
    # App URLs
    path("", include(app_urls)),
]
