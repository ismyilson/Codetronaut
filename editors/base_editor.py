import abc


class UnsupportedEditor(Exception):
    def __init__(self, message):
        super().__init__(message)


class BaseEditor(abc.ABC):
    identifiers: list[str]
    name: str
    exe_name: str

    def go_to_file(self, file):
        pass
