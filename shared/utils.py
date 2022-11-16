import math
from typing import List
import numpy as np

from shared.element import Element


def split_list(list_to_split):
    """
    Split list in half

    Arguments:
        list_to_split(List): list which will be split

    Returns:
        tuple of lists
    """
    half = math.ceil(len(list_to_split) / 2)
    return list_to_split[:half], list_to_split[half:]


def choose_best_knapsack(knapsacks: List[List[bool]], elements: List[Element]):
    """
    Choose the best knapsack

    Arguments:
        knapsacks(List[List[bool]]): list of knapsacks
        elements(List[Element]): list of elements to pack to knapsack

    Returns:
        the best knapsack
    """
    sorted_knapsacks = knapsacks.copy()
    sorted_knapsacks.sort(
        key=lambda knapsack: calculate_profits_sum(knapsack, elements),
        reverse=True)
    return sorted_knapsacks[0]


def choose_best_knapsack_capacity(knapsacks: List[List[bool]], elements: List[Element], capacity: int):
    """
    Choose the best knapsack under capacity

    Arguments:
        knapsacks(List[List[bool]]): list of knapsacks
        elements(List[Element]): list of elements to pack to knapsack

    Returns:
        the best knapsack
    """
    sorted_knapsacks = knapsacks.copy()
    sorted_knapsacks.sort(
        key=lambda knapsack: calculate_profits_sum(knapsack, elements)*math.copysign(1, 1 + capacity - calculate_weights_sum(knapsack, elements)),
        reverse=True)
    return sorted_knapsacks[0]


def calculate_weights_sum(x: List[bool], elements: List[Element]):
    """
    Calculate knapsack's weight

    Arguments:
        x(List[bool]): list of boolean values which define if element will be pack into knapsack
        elements(List[Element]): list of elements to pack to knapsack

    Returns:
        knapsack's weight
    """
    return sum(xi * element.weight for xi, element in zip(x, elements))


def calculate_profits_sum(x: List[bool], elements: List[Element]):
    """
    Calculate knapsack's worth

    Arguments:
        x(List[bool]): list of boolean values which define if element will be pack into knapsack
        elements(List[Element]): list of elements to pack to knapsack

    Returns:
        knapsack's worth
    """
    return sum(xi * element.profit for xi, element in zip(x, elements))


def get_weights_list(elements: List[Element]):
    return [element.weight for element in elements]


def get_profits_list(elements: List[Element]):
    return [element.profit for element in elements]
