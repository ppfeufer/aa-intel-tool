"""
Test for the data_structures helper => aa_intel_tool/helper/data_structure.py
"""

# Django
from django.test import TestCase

# AA Intel Tool
from aa_intel_tool.helper.data_structure import dict_to_list


class TestHelperDataStructures(TestCase):
    """
    Test the data_structures helper
    """

    def test_dict_to_list(self):
        """
        Test that we get a list from a dict

        :return:
        :rtype:
        """

        my_dict = {
            "foobar": {"foo": "bar", "bar": "foo"},
            "barfoo": {"bar": "foo", "foo": "bar"},
        }
        my_list = dict_to_list(my_dict)
        expected_list = [{"bar": "foo", "foo": "bar"}, {"foo": "bar", "bar": "foo"}]

        self.assertListEqual(list1=my_list, list2=expected_list)
