from pathlib import Path

import pickle


def write_to_file(path, data):
    try:
        dir_path = path[0:path.rindex('\\')]
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    except ValueError:
        pass

    with open(path, 'wb') as file:
        pickle.dump(data, file)


def load_file(path):
    with open(path, 'rb') as file:
        data = pickle.load(file)
        return data
