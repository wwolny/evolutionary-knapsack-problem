import argparse
import pandas as pd
import time

from algorithms.AR import AR
from algorithms.PBIL import PBIL
from shared import validators
from shared import utils
import shared.db as db

parser = argparse.ArgumentParser()
parser.add_argument("--algorithm", type=validators.check_algorithm_type, default="PBIL",
                    help="Specify the algorithm: PBIL, AR")
parser.add_argument("--dataset_file", type=validators.check_dataset_path,
                    help="Specify the dataset filename")
parser.add_argument("--epochs", type=validators.check_positive_integer, default=100,
                    help="Specify number of epochs")
parser.add_argument("--repeat", type=validators.check_positive_integer, default=20,
                    help="Specify number of repetition")
parser.add_argument("--capacity", type=validators.check_positive_integer, default=100,
                    help="Specify knapsack capacity")
parser.add_argument("--penalty", type=validators.check_PBIL_penalty, default="log",
                    help="Specify penalty type for PBIL algorithm")
parser.add_argument("--M", type=validators.check_positive_integer, default=10,
                    help="Specify parameter M")
parser.add_argument("--N", type=validators.check_positive_integer, default=5,
                    help="Specify parameter N")
parser.add_argument("--lr", type=validators.check_positive_float, default=0.1,
                    help="Specify parameter learning rate")
parser.add_argument("--c", type=validators.check_positive_integer, default=0.05,
                    help="Specify probability of change knapsack to repair version")
parser.add_argument("--i", type=validators.check_positive_integer, default=0.5,
                    help="Specify probability of inheritance True or False value when knapsack's parent have different values")
parser.add_argument("--p", type=validators.check_positive_integer, default=0.15,
                    help="Specify probability of negating of the value in knapsack")
args = parser.parse_args()

if __name__ == '__main__':
    print("algorithm " + str(args.algorithm))
    print("dataset file " + str(args.dataset_file))
    print("epochs " + str(args.epochs))
    print("capacity " + str(args.capacity))
    print("repeat " + str(args.repeat))
    data = db.load_database(args.dataset_file)

    if args.algorithm == "PBIL":
        algorithm = PBIL(penalty=args.penalty, M=args.M, N=args.N, lr=args.lr)
        filename = "-".join([str(el) for el in [args.dataset_file, args.epochs, args.capacity, args.repeat, args.algorithm, args.penalty, args.M, args.N, args.lr]])
    else:
        algorithm = AR(M=args.M, c=args.c, i=args.i, p=args.p)
        filename = "-".join([str(el) for el in [args.dataset_file, args.epochs, args.capacity, args.repeat, args.algorithm, args.M, args.c, args.i, args.p]])
    print(filename)
    best_kanpsacks = []
    for _ in range(args.repeat):
        s_time = time.time()
        algorithm.run(elements=data, capacity=args.capacity, epochs=args.epochs)
        e_time = time.time()
        best_kanpsacks.append({"weight": utils.calculate_weights_sum(algorithm.best_knapsacks, data),
                               "profit": utils.calculate_profits_sum(algorithm.best_knapsacks, data),
                               "time": e_time-s_time})
    df_out = pd.DataFrame(best_kanpsacks)
    df_out.to_csv("results/"+filename, index=False)
