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

    return [
        data
        for (
            not_used,  # pylint: disable=unused-variable
            data,
        ) in sorted(input_dict.items())
    ]
