import argparse
import generator.generator as generator
import shared.db as db

from shared import validators

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=validators.check_data_type, default="u",
                    help="Specify the type of data: u - uncorrelated, w - weakly correlated, s - strongly correlated")
parser.add_argument("--elem_amount", type=validators.check_positive_integer, default=100,
                    help="Specify number of elements which will be generated")
parser.add_argument("--max_weight", dest="v", type=validators.check_positive_integer, default=10,
                    help="Specify maximum weight")
parser.add_argument("--max_prof_deviation", dest="r", type=validators.check_positive_integer, default=5,
                    help="Specify maximum deviation between weight and profit")
args = parser.parse_args()

if __name__ == '__main__':
    print("type " + str(args.type))
    print("elem_amount " + str(args.elem_amount))
    print("v (max_weight) " + str(args.v))
    print("r (max_prof_deviation) " + str(args.r))

    data = generator.generate_data(args.type, args.elem_amount, args.v, args.r)
    file_name = db.generate_file_name(args.type, args.elem_amount, args.v, args.r)
    db.save_database(data, file_name)

    new_data = db.load_database(file_name)
    for elem in new_data:
        print(elem.weight, elem.profit)

