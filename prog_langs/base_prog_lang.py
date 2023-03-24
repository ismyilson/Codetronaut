import abc

from pynput.keyboard import Key

import writer as wr


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

    def set_variable_initial_value(self, line, var_name, var_value):
        pass

    def set_variable(self, var_name, var_value):
        pass

    def find_variable(self, lines, var_name):
        pass

    def find_method(self, lines, method_name):
        pass

    def add_if_condition(self, first_part, operation, second_part):
        pass

    def add_return(self, value):
        pass

    def add_call_method(self, method):
        pass

    def _write_code(self, code, add_semicolon, add_extra_blank=True):
        code_lines = code.split('\n')
        added_lines = 0

        writer = wr.Writer()
        for line in code_lines:
            for word in line:
                writer.add_text(word)

                if word == '}':
                    writer.add_key(Key.left)

            if line != code_lines[-1]:
                writer.add_key(Key.enter)
                added_lines += 1

        if add_semicolon and self.requires_semicolon:
            writer.add_text(';')

        if add_extra_blank:
            writer.add_key(Key.enter)
            added_lines += 1

        writer.execute()

        return added_lines
