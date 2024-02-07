"""
Tests for the template tags
"""

# Django
from django.test import TestCase

# AA Intel Tool
from aa_intel_tool import __version__
from aa_intel_tool.tests.utils import render_template


class TestForumVersionedStatic(TestCase):
    """
    Tests for inteltool_versioned_static template tag
    """

    def test_versioned_static(self):
        """
        Test should return static URL string with a version
        :return:
        """

        context = {"version": __version__}

        rendered_template = render_template(
            string=(
                "{% load inteltool_versioned_static %}"
                "{% aa_intel_tool_static 'aa_intel_tool/css/aa-intel-tool.min.css' %}"
            ),
            context=context,
        )

        self.assertEqual(
            rendered_template,
            f'/static/aa_intel_tool/css/aa-intel-tool.min.css?v={context["version"]}',
        )
