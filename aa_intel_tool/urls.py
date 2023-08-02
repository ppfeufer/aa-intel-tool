"""
our urls
"""

# Django
# from django.conf.urls import url
from django.urls import path, re_path

# AA Intel Tool
from aa_intel_tool import views

app_name: str = "aa_intel_tool"

urlpatterns = [
    path(route="", view=views.index, name="intel_tool_index"),
    re_path(
        route=r"^(?P<scan_hash>[a-zA-Z0-9]+)/$", view=views.scan, name="intel_tool_scan"
    ),
]
