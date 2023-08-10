"""
Test URL config
"""

# Django
from django.urls import include, path

# Alliance Auth
from allianceauth import urls

# Alliance auth urls
urlpatterns = [
    path("", include(urls)),
]
