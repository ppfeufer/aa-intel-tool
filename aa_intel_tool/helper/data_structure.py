"""
Helper for different data structures
"""


def dict_to_list(input_dict: dict) -> list:
    """
    Cleaning up and sorting a dict and transform it into a list

    :param input_dict: A dict to be cleaned up and sorted
    :type input_dict: dict
    :return: A list of the values of the input dict, sorted by their keys
    :rtype: list
    """

    return list(dict(sorted(input_dict.items())).values())
