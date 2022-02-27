"""
hook into AA
"""

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook

# AA Intel Tool
from aa_intel_tool import __title__


class AaIntelToolMenuItem(MenuItemHook):  # pylint: disable=too-few-public-methods
    """
    This class ensures only authorized users will see the menu entry
    """

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _(__title__),
            "fas fa-clipboard-list fa-fw",
            "aa_intel_tool:intel_tool_index",
            navactive=["aa_intel_tool:"],
        )

    def render(self, request):
        """
        check if the user has the permission to view this app
        :param request:
        :return:
        """

        return MenuItemHook.render(self, request)


@hooks.register("menu_item_hook")
def register_menu():
    """
    register our menu item
    :return:
    """

    return AaIntelToolMenuItem()
