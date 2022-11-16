from __future__ import annotations

from typing import List


class Element:
    """
    Class of element using in knapsack problem.
    """

    def __init__(self, weight, profit):
        """
        Simple constructor of class Element.

        weight(int): Element's weight
        profit(int) Element's profit
        """

        self.weight = weight
        self.profit = profit
