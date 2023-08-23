"""
Helper for different data structures
"""


def dict_to_list(input_dict: dict) -> list:
    """
    Cleaning up and sorting a dict and transform it into a list

    :param input_dict:
    :type input_dict:
    :return:
    :rtype:
    """

    return list(dict(sorted(input_dict.items())).values())
