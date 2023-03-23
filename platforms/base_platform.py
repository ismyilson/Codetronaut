import abc
import psutil
import json
import os
import pathlib


class UnsupportedPlatform(Exception):
    def __init__(self, message):
        super().__init__(message)


class BasePlatform(abc.ABC):
    identifier: str
    name: str

    def run(self, file, *args, from_dir=None):
        if from_dir is None:
            process = psutil.Popen([file, *args])
        else:
            process = psutil.Popen([file, *args], cwd=from_dir)

        return process

    def close(self, pid):
        try:
            process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            return

        process.terminate()

    def create_file(self, file_name, root_dir=''):
        path = os.path.join(root_dir, file_name)
        path = os.path.expandvars(path)

        f = open(path, 'x')
        f.close()

    def file_exists(self, file_name, root_dir=''):
        path = os.path.join(root_dir, file_name)
        path = os.path.expandvars(path)

        return os.path.isfile(path)

    def write_file(self, path, data, to_json=False):
        path = os.path.expandvars(path)

        self.create_directories_to_file(path)

        with open(path, 'w' if to_json else 'wb') as file:
            if to_json:
                json.dump(data, file, indent=2)
            else:
                file.write(data)

    def read_file(self, path, is_json=False):
        path = os.path.expandvars(path)

        with open(path, 'r' if is_json else 'rb') as file:
            if is_json:
                return json.load(file)
            else:
                return file.read()

    def create_directories_to_file(self, path, parents=True, exist_ok=True):
        idx = path.rfind('\\')
        if idx == -1:
            idx = path.rfind('/')

        if idx == -1:
            return

        dir_path = path[:idx]
        pathlib.Path(dir_path).mkdir(parents=parents, exist_ok=exist_ok)

    def get_files_in_directory(self, path):
        files = []

        for p in os.listdir(path):
            if os.path.isfile(os.path.join(path, p)):
                files.append(os.path.splitext(p))

        return files

    def get_file_lines(self, file):
        with open(file, 'r') as f:
            return f.readlines()

    def get_file_line_count(self, file):
        return sum(1 for line in open(file, 'r'))

    def get_install_path(self, name):
        pass

    def focus(self, pid):
        pass
