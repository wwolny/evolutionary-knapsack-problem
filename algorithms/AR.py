from typing import List

import numpy as np

from algorithms.interface import AlgorithmInterface
from shared import utils
from shared.element import Element


class AR(AlgorithmInterface):
    """
    Implementation of evolutionary algorithm based on Ar (greedy) algorithm.
    """

    def __init__(self, M: int = 10, c: float = 0.05, i: float = 0.5, p: float = 0.15):
        self.probability_vector = None
        self.M = M
        self.c = c
        self.i = i
        self.p = p
        self.best_knapsacks = []

    def run(self, elements: list, capacity: int, epochs: int = 100, M: int = None, c: float = None, i: float = None,
            p: float = None):
        """
        Run algorithm for given dataset

        Arguments:
            elements(List[Element]): list of elements to pack to knapsack
            capacity(int): maximal capacity od knapsack
            epochs(int): number of epochs to iterate over
            M(int): number of elements in each epoch
            c(float): probability of change knapsack to repair version
            i(float): probability of inheritance True or False value when knapsack's parent have different values
            p(float): probability of negating of the value in knapsack

        Returns:
            the best knapsack
        """
        self.M = M if M is not None else self.M
        self.c = c if c is not None else self.c
        self.i = i if i is not None else self.i
        self.p = p if p is not None else self.p
        self.probability_vector = super(AR, self)._generate_probability_vector(len(elements))
        knapsacks = [super(AR, self)._generate_knapcack(self.probability_vector) for _ in range(self.M)]
        for _ in range(epochs):
            repaired_knapsacks = [self.__repair(knapsack, elements, capacity) for knapsack in knapsacks]
            final_knapsacks = self.__replace_knapsacks(knapsacks, repaired_knapsacks)
            knapsacks = self.__generate_new_population(final_knapsacks, elements)
            self.best_knapsacks = utils.choose_best_knapsack_capacity(knapsacks, elements, capacity)
        return self.best_knapsacks

    def __repair(self, knapsack: List[bool], elements: List[Element], capacity: int):
        """
        Repair knapsack

        Arguments:
            knapsack(List[bool]): list of boolean values which define if element will be pack into knapsack
            elements(List[Element]): list of elements to pack to knapsack
            capacity(int): maximal capacity od knapsack

        Returns:
            repaired knapsack
        """
        repaired_knapsack = knapsack.copy()
        weights_sum = utils.calculate_weights_sum(repaired_knapsack, elements)
        while weights_sum > capacity:
            i = self.__select_item_to_remove(repaired_knapsack, elements)
            repaired_knapsack[i] = False
            weights_sum = utils.calculate_weights_sum(repaired_knapsack, elements)

        return repaired_knapsack

    def __select_item_to_remove(self, knapsack: List[bool], elements: List[Element]):
        """
        Select item to remove from knapsack - greedy approach

        Arguments:
            knapsack(List[bool]): list of boolean values which define if element will be pack into knapsack
            elements(List[Element]): list of elements to pack to knapsack

        Returns:
            index of element which will be removed
        """
        sorted_elements = [elem for (elem, xi) in zip(elements, knapsack) if xi is True]
        sorted_elements.sort(key=lambda elem: elem.profit / elem.weight)

        return elements.index(sorted_elements[0])

    def __replace_knapsacks(self, knapsacks: List[List[bool]], repaired_knapsacks: List[List[bool]]):
        """
        Replace knapsack

        Arguments:
            knapsacks(List[List[bool]]): list of knapsacks
            repaired_knapsacks(List[List[bool]]): list of repaired knapsacks

        Returns:
            list of final knapsacks
        """
        return [repaired_knapsack if np.random.random() <= self.c else knapsack
                for (knapsack, repaired_knapsack) in zip(knapsacks, repaired_knapsacks)]

    def __generate_new_population(self, knapsacks: List[List[bool]], elements: List[Element]):
        """
        Generate new population of knapsacks

        Arguments:
            knapsacks(List[List[bool]]): list of knapsacks
            elements(List[Element]): list of elements to pack to knapsack

        Returns:
            new generation of knapsacks
        """
        sorted_knapsacks = knapsacks.copy()
        sorted_knapsacks.sort(key=lambda knapsack: utils.calculate_profits_sum(knapsack, elements), reverse=True)
        final_knapsacks, worse_knapsacks = utils.split_list(sorted_knapsacks)

        worse_knapsacks = self.__cross_knapsacks(final_knapsacks, worse_knapsacks)
        final_knapsacks.extend(worse_knapsacks)
        return final_knapsacks

    def __cross_knapsacks(self, better_knapsacks: List[List[bool]], worse_knapsacks: List[List[bool]]):
        """
        Cross multiple knapsacks

        Arguments:
            better_knapsacks(List[List[bool]]): list of 50% the best knapsacks
            worse_knapsacks(List[List[bool]]): list of 50% worse knapsacks

        Returns:
            crossed knapsacks
        """
        worse_knapsacks.reverse()
        for better, worse in zip(better_knapsacks, worse_knapsacks):
            worse = self.__cross(better, worse)

        return worse_knapsacks

    def __cross(self, better: List[bool], worse: List[bool]):
        """
        Cross knapsacks

        Arguments:
            better(List[bool]): better knapsack
            worse(List[bool]): worse knapsack

        Returns:
            final knapsack
        """
        crossed = []
        for first, second in zip(better, worse):
            if first and second:
                element = True
            elif not first and not second:
                element = False
            else:
                element = True if np.random.random() < self.i else False
            element = not element if np.random.random() < self.p else element
            crossed.append(element)
        return crossed
