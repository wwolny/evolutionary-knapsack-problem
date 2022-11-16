import argparse
import os


def check_positive_integer(value):
    """
    Validate data if it's positive integer type.

    Arguments:
        value: Data which will be validated

    Returns:
        Correct value
    """

    int_value = int(value)
    if int_value <= 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid integer value, positive values required" % value)
    return int_value


def check_data_type(value):
    """
    Validate data if it's one of three types (u, w or s).

    Arguments:
        value: Data which will be validated

    Returns:
        Correct value
    """

    correct_types = ["u", "w", "s"]
    string_value = str(value)

    if string_value not in correct_types:
        raise argparse.ArgumentTypeError(
            "%r is not a correct data type" % string_value)

    return string_value


def check_algorithm_type(value):
    """
    Validate data if it's one of two types (PBIL, AR).

    Arguments:
        value: Data which will be validated

    Returns:
        Correct value
    """

    correct_types = ["PBIL", "AR"]
    string_value = str(value)

    if string_value not in correct_types:
        raise argparse.ArgumentTypeError(
            "%r is not a correct algorithm type" % string_value)

    return string_value


def check_dataset_path(value):
    """
    Validate data if it's dataset path.

    Arguments:
        value: Data which will be validated

    Returns:
        Correct value
    """
    string_value = str(value)

    if not os.path.isfile("./db/" + string_value):
        raise argparse.ArgumentTypeError(
            "%r is not a correct dataset path" % string_value)

    return string_value


def check_PBIL_penalty(value):
    """
    Validate data if it's one of three types (log, "lin, qua).

    Arguments:
        value: Data which will be validated

    Returns:
        Correct value
    """

    correct_types = ["log", "lin", "qua"]
    string_value = str(value)

    if string_value not in correct_types:
        raise argparse.ArgumentTypeError(
            "%r is not a correct PBIL penalty" % string_value)

    return string_value


def check_positive_float(value):
    """
    Validate data if it's positive float type.

    Arguments:
        value: Data which will be validated

    Returns:
        Correct value
    """

    float_value = float(value)
    if float_value <= 0.0 or float_value > 1.0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid integer value, positive values required" % value)
    return float_value
