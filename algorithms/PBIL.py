from algorithms.interface import AlgorithmInterface
from shared import utils
from shared.element import Element

from typing import AnyStr, List
import numpy as np


class PBIL(AlgorithmInterface):
    """
    Implementation of PBIL algorithm.
    """

    def __init__(self, penalty: AnyStr = "log", M: int = 10, N: int = 5, lr: float = 0.1):
        self.probability_vector = None
        self.M = M
        self.N = N
        self.lr = lr
        self.penalty = penalty

    def run(self, elements: List[Element], capacity: int, penalty: AnyStr = None,
            epochs: int = 100, M: int = None,
            N: int = None, lr: float = None):
        """
        Run PBIL algorithm for given dataset

        Arguments:
            elements(List[Element]): list of elements to pack to knapsack
            capacity(int): maximal capacity od knapsack
            penalty(AnyStr): type of penalty choose from: ["log", "lin", "qua"]
            epochs(int): number of epochs to iterate over
            M(int): number of elements to generate in each epoch
            N(int): number of best elements to modify probability vector
            lr(float): learning_rate for probability vector

        Returns:
            the best knapsack
        """
        self.probability_vector = super(PBIL, self)._generate_probability_vector(len(elements))
        self.M = M if M is not None else self.M
        self.N = N if N is not None else self.N
        self.lr = lr if lr is not None else self.lr
        self.penalty = penalty if penalty is not None else self.penalty
        if self.N > self.M:
            raise ValueError
        for _ in range(epochs):
            knapsacks = [
                super(PBIL, self)._generate_knapcack(self.probability_vector)
                for
                _ in range(self.M)]
            eval_kanpsacks = self._eval_knapsacks(elements, knapsacks, capacity,
                                                  penalty=self.penalty)
            zipped_knapsacks = zip(knapsacks, eval_kanpsacks)
            sorted_knapsacks = sorted(zipped_knapsacks, key=lambda x: x[1])
            n_best_knapsacks = sorted_knapsacks[-1*self.N:]
            new_prob_vector = []
            for id_, old_prob in enumerate(self.probability_vector):
                new_val = (1 - self.lr) * old_prob + self.lr * (1 / self.N) * sum(
                    [knapsack[0][id_] for knapsack in n_best_knapsacks])
                new_prob_vector.append(new_val)
            self.probability_vector = new_prob_vector
            self.best_knapsacks = utils.choose_best_knapsack_capacity(knapsacks, elements, capacity)
        return self.best_knapsacks

    def _eval_knapsacks(self, elements: List[Element], knapsacks: List[List[bool]], capacity: int,
                        penalty: AnyStr = "log"):
        """
        Evaluate knapsack

        Arguments:
            knapsacks(List[List[bool]]): list of lists of boolean values which \
            define if element will be pack into knapsack
            elements(List[Element]): list of elements to pack to knapsack
            capacity(int): maximal capacity od knapsack
            penalty(AnyStr): name of penalty type

        Returns:
            List[float]: list of evaluation values for each knapsack
        """
        eval_val = []
        for knapsack in knapsacks:
            tmp_eval = utils.calculate_profits_sum(knapsack, elements)\
                       - self._penalty_value(penalty, elements, knapsack, capacity)
            eval_val.append(tmp_eval)
        return eval_val

    def _penalty_logarithmic(self, elements, knapsack, capacity):
        return np.log2(1 + self._calculate_rho(elements, knapsack) * (
                    utils.calculate_weights_sum(knapsack, elements) - capacity))

    def _penalty_linear(self, elements, knapsack, capacity):
        return self._calculate_rho(elements, knapsack) * (
                    utils.calculate_weights_sum(knapsack, elements) - capacity)

    def _penalty_quadratic(self, elements, knapsack, capacity):
        return (self._calculate_rho(elements, knapsack) * (
                    utils.calculate_weights_sum(knapsack,
                                                elements) - capacity)) ** 2

    def _penalty_value(self, penalty_type: AnyStr, elements, knapsack,
                       capacity):
        if utils.calculate_weights_sum(knapsack, elements) <= capacity:
            return 0
        if penalty_type == "log":
            return self._penalty_logarithmic(elements, knapsack, capacity)
        elif penalty_type == "lin":
            return self._penalty_linear(elements, knapsack, capacity)
        elif penalty_type == "qua":
            return self._penalty_quadratic(elements, knapsack, capacity)
        else:
            raise ValueError

    def _calculate_rho(self, elements, knapsack):
        return max([xi * (element.profit / element.weight) for xi, element in
                    zip(knapsack, elements)])
