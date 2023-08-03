"""
Our URL config
"""

# Django
from django.urls import include, path, re_path

# AA Intel Tool
from aa_intel_tool.views import general

app_name: str = "aa_intel_tool"


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
    # App URLs
    path("", include(app_urls)),
]
