"""
Hook into AA
"""

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Intel Tool
from aa_intel_tool import __title__, urls


class AaIntelToolMenuItem(MenuItemHook):  # pylint: disable=too-few-public-methods
    """
    This class ensures only authorized users will see the menu entry
    """

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            text=__title__,
            classes="fa-solid fa-clipboard-list",
            url_name="aa_intel_tool:intel_tool_index",
            navactive=["aa_intel_tool:"],
        )

    def render(self, request):
        """
        Render the menu item

        :param request:
        :type request:
        :return:
        :rtype:
        """

        return MenuItemHook.render(self, request=request)


@hooks.register(name="menu_item_hook")
def register_menu():
    """
    Register our menu item

    :return:
    :rtype:
    """

    return AaIntelToolMenuItem()


@hooks.register(name="url_hook")
def register_urls():
    """
    Register our base url

    :return:
    :rtype:
    """

    return UrlHook(
        urls=urls,
        namespace="aa_intel_tool",
        base_url=r"^intel/",
        excluded_views=[
            "aa_intel_tool.views.ajax.get_scan_data",
            "aa_intel_tool.views.general.index",
            "aa_intel_tool.views.general.scan",
        ],
    )
