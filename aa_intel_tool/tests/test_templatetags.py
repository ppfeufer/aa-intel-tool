"""
Tests for the template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase, override_settings

# AA Intel Tool
from aa_intel_tool import __version__
from aa_intel_tool.helper.static_files import calculate_integrity_hash


class TestVersionedStatic(TestCase):
    """
    Tests for aa_intel_tool template tag
    """

    @override_settings(DEBUG=False)
    def test_versioned_static(self):
        """
        Test should return static URL string with a version
        :return:
        """

        context = Context(dict_={"version": __version__})

        template_to_render = Template(
            template_string=(
                "{% load aa_intel_tool %}"
                "{% aa_intel_tool_static 'css/aa-intel-tool.min.css' %}"
                "{% aa_intel_tool_static 'javascript/aa-intel-tool.min.js' %}"
            )
        )

        rendered_template = template_to_render.render(context=context)

        expected_static_css_src = (
            f'/static/aa_intel_tool/css/aa-intel-tool.min.css?v={context["version"]}'
        )
        expected_static_css_src_integrity = calculate_integrity_hash(
            "css/aa-intel-tool.min.css"
        )
        expected_static_js_src = f'/static/aa_intel_tool/javascript/aa-intel-tool.min.js?v={context["version"]}'
        expected_static_js_src_integrity = calculate_integrity_hash(
            "javascript/aa-intel-tool.min.js"
        )

        self.assertIn(member=expected_static_css_src, container=rendered_template)
        self.assertIn(
            member=expected_static_css_src_integrity, container=rendered_template
        )
        self.assertIn(member=expected_static_js_src, container=rendered_template)
        self.assertIn(
            member=expected_static_js_src_integrity, container=rendered_template
        )

    @override_settings(DEBUG=True)
    def test_versioned_static_with_debug_enabled(self) -> None:
        """
        Test versioned static template tag with DEBUG enabled

        :return:
        :rtype:
        """

        context = Context({"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load aa_intel_tool %}"
                "{% aa_intel_tool_static 'css/aa-intel-tool.min.css' %}"
            )
        )

        rendered_template = template_to_render.render(context=context)

        expected_static_css_src = (
            f'/static/aa_intel_tool/css/aa-intel-tool.min.css?v={context["version"]}'
        )

        self.assertIn(member=expected_static_css_src, container=rendered_template)
        self.assertNotIn(member="integrity=", container=rendered_template)
