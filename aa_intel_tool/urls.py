"""
our urls
"""

# Django
# from django.conf.urls import url
from django.urls import path

# AA Intel Tool
from aa_intel_tool import views

app_name: str = "aa_intel_tool"

urlpatterns = [
    path("", views.index, name="intel_tool_index"),
    # url(r"^(?P<scan_hash>[a-zA-Z0-9]+)/$", views.scan, name="intel_tool_scan"),
]
