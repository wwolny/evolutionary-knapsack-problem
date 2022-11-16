from typing import List
import numpy as np

from shared.element import Element


class AlgorithmInterface:
    """
    Interface class for algorithms.
    """

    def run(self, elements: List[Element], capacity: int, epochs: int = 100) -> dict:
        """
        Run algorithm for given dataset.

        Arguments:
            elements(List[Element]): list of elements to pack to knapsack.
            capacity(int): maximal capacity od knapsack
            epochs(int): number of epochs to iterate over.

        Returns:
            dict with results of the best solution after each epoch.
        """
        pass

    def _generate_probability_vector(self, elem_amount: int):
        """
        Generate probability vector: 50% for each element

        Arguments:
            elem_amount(int): Amount of generated elements

        Returns:
            List of probability
        """
        return [0.5] * elem_amount

    def _generate_knapcack(self, probability_vector: List[float]):
        """
        Generate knapsack vector by probability vector

        Arguments:
            probability_vector(List[float]): Probability vector

        Returns:
            Knapsack - list of boolean values, which represent if elements are in knapsack
        """
        return [np.random.random() <= prob for prob in probability_vector]
