import abc


class UnsupportedProgrammingLanguage(Exception):
    def __init__(self, message):
        super().__init__(message)


class BaseProgrammingLanguage(abc.ABC):
    identifiers: list[str]
    name: str

    extensions: list[str]

    def create_class(self, name):
        pass
