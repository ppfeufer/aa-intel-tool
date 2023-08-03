"""
our urls
"""

# Django
# from django.conf.urls import url
from django.urls import include, path, re_path

# AA Intel Tool
from aa_intel_tool.constants import INTERNAL_URL_PREFIX
from aa_intel_tool.views import ajax, general

app_name: str = "aa_intel_tool"

ajax_urls = [
    path(
        route="parse-form-data",
        view=ajax.parse_form_data,
        name="ajax_parse_form_data",
    ),
]

app_urls = [
    path(route="", view=general.index, name="intel_tool_index"),
    re_path(
        route=r"^(?P<scan_hash>[a-zA-Z0-9]+)/$",
        view=general.scan,
        name="intel_tool_scan",
    ),
]

# Put it all together
urlpatterns = [
    # Ajax URLs
    path(f"{INTERNAL_URL_PREFIX}/ajax/", include(ajax_urls)),
    # App URLs
    path("", include(app_urls)),
]
