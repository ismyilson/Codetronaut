import abc

import keyboard


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

    def create_method(self, name, access_type, is_static, ret_type):
        pass

    def create_variable(self, var_type, var_name):
        pass

    def set_variable(self, line, var_name, var_value):
        pass

    def find_variable(self, lines, var_name):
        pass

    def _write_code(self, code, add_semicolon):
        code_lines = code.split('\n')

        for line in code_lines:
            for word in line:
                keyboard.write(word)

                if word == '}':
                    keyboard.press('left arrow, return')

            if line != code_lines[-1]:
                keyboard.press('return')

        if add_semicolon and self.requires_semicolon:
            keyboard.write(';')

        keyboard.press('intro')
