import abc

from pynput.keyboard import Key

import writer as wr


class UnsupportedEditor(Exception):
    def __init__(self, message):
        super().__init__(message)


class BaseEditor(abc.ABC):
    identifiers: list[str]
    name: str
    exe_name: str

    def new_line(self):
        writer = wr.Writer()

        writer.add_key(Key.enter)

        writer.execute()

    def go_to_file(self, file):
        pass

    def go_to_line(self, line, column=10000):
        pass

    def save_file(self):
        pass

    def save_all_files(self):
        pass

    def refactor_rename(self, new_name):
        pass

    def select_line(self, line):
        pass
