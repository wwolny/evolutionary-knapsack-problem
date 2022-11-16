import pickle


def generate_file_name(data_type, elem_amout, v, r):
    return f"{data_type}_{elem_amout}_{v}_{r}"


def save_database(database, file_path):
    with open(f"db/{file_path}", 'wb') as f:
        pickle.dump(database, f)
    print("database saved")


def load_database(file_path):
    with open(f"db/{file_path}", 'rb') as f:
        return pickle.load(f)
