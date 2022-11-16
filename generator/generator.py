import numpy as np

from shared.element import Element


def generate_data(data_type, elem_amount, v, r):
    """
    Generate data for knapsack problem.

    Arguments:
        data_type(str): Type of data: u - uncorrelated, w - weakly correlated, s - strongly correlated
        elem_amount(int): Amount of generated elements
        v(int): Maximum elements' weight
        r(int): Maximum deviation between weight and profit

    Returns:
        List of elements
    """

    if data_type == "u":
        generate = generate_uncorrelated_data
    elif data_type == "w":
        generate = generate_weakly_correlated_data
    else:
        generate = generate_strongly_correlated_data

    data = []
    for _ in range(elem_amount):
        data.append(generate(v, r))

    return data


def generate_uncorrelated_data(v, r):
    """
    Generate element of uncorrelated data.

    Arguments:
        v(int): Maximum element's weight
        r(int): Maximum deviation between weight and profit

    Returns:
        Uncorrelated element
    """

    weight = np.random.random_integers(1, v)
    profit = np.random.random_integers(1, v)
    return Element(weight, profit)


def generate_weakly_correlated_data(v, r):
    """
    Generate element of weakly correlated data.

    Arguments:
        v(int): Maximum element's weight
        r(int): Maximum deviation between weight and profit

    Returns:
        Weakly correlated element
    """

    weight = np.random.random_integers(1, v)
    min_r = -(weight - 1) if r >= weight else -r
    profit = weight + np.random.random_integers(min_r, r)
    return Element(weight, profit)


def generate_strongly_correlated_data(v, r):
    """
    Generate element of strongly correlated data.

    Arguments:
        v(int): Maximum element's weight
        r(int): Deviation between weight and profit

    Returns:
        Strongly correlated element
    """

    weight = np.random.random_integers(1, v)
    profit = weight + r
    return Element(weight, profit)
