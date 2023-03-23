import abc

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

        writer.add_hotkey('enter')

        writer.execute()

    def go_to_file(self, file):
        pass

    def go_to_line(self, line):
        pass

    def save_file(self):
        pass

    def save_all_files(self):
        pass

    def delete_lines(self, line_start, line_end):
        pass
