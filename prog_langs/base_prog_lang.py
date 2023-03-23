import abc


class UnsupportedProgrammingLanguage(Exception):
    def __init__(self, message):
        super().__init__(message)


class BaseProgrammingLanguage(abc.ABC):
    identifiers: list[str]
    name: str

    extensions: list[str]

    requires_semicolon: bool

    def create_class(self, name):
        pass

    def create_variable(self, var_type, var_name):
        pass

    def set_variable(self, line, var_name, var_value):
        pass

    def find_variable(self, lines, var_name):
        pass
