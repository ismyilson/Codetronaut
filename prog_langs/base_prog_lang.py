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
        var_name = var_name.lower()
        for idx, line in enumerate(lines):
            lower_line = line.lower()

            if var_name in lower_line:
                try:
                    var_col = lower_line.index(var_name) + 1
                except IndexError:
                    continue

                if var_col == 0:
                    continue

                return {
                    'line': idx + 1,
                    'var_col': var_col
                }

        return None

    def find_method(self, lines, method_name):
        method_name = method_name.lower()
        for idx, line in enumerate(lines):
            lower_line = line.lower()

            if method_name in lower_line:
                parenthesis_open_idx = line.rindex('(')
                parenthesis_close_idx = line.rindex(')')

                method_name = line[line.rindex(' ') + 1:parenthesis_open_idx]

                params_col = parenthesis_close_idx + 1
                params_line = line[parenthesis_open_idx + 1:parenthesis_close_idx]

                params = []
                if ',' in params_line:
                    params = [params_line.split(',')]
                else:
                    if params_line != '':
                        params = [params_line]

                return {
                    'name': method_name,
                    'line': idx + 1,
                    'params_col': params_col,
                    'params': params
                }

        return None

    def add_if_condition(self, first_part, operation, second_part):
        pass

    def add_return(self, params):
        pass

    def add_call_method(self, method):
        pass

    def add_print(self, args):
        pass

    def add_parameter_to_method(self, param_list, var_type, var_name):
        pass

    def _write_code(self, code, add_semicolon):
        code_lines = code.split('\n')
        added_lines = 0

        writer = wr.Writer()
        for line in code_lines:
            for word in line:
                writer.add_text(word)

                if word == '}':
                    writer.add_key(Key.left)
                    writer.add_key(Key.enter)

            if line != code_lines[-1]:
                writer.add_key(Key.enter)
                added_lines += 1

        if add_semicolon and self.requires_semicolon:
            writer.add_text(';')

        writer.execute()

        return added_lines
