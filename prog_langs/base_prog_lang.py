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
                var_data = self._extract_var_data(line, var_name, idx + 1)

                if var_data is None:
                    continue

                return var_data

        return None

    def _extract_var_data(self, line, name, line_idx):
        words = line.replace(';', '').split()

        name_idx = -1
        assignation_idx = -1
        is_static = False
        access_type = None
        for idx, word in enumerate(words):
            if word.lower() == name:
                name_idx = idx
                continue

            if word == '=':
                assignation_idx = idx
                continue

            if word == 'static':
                is_static = True
                continue

            if word in ['public', 'private', 'protected']:
                access_type = word
                continue

        if name_idx == -1:
            return None

        var_name = words[name_idx]
        var_type = words[name_idx - 1] if name_idx != 0 else None
        var_value = ''.join(words[assignation_idx + 1:]) if assignation_idx != -1 else None
        var_idx = line.lower().index(name)
        return {
            'name': var_name,
            'type': var_type,
            'value': var_value,
            'static': is_static,
            'access_type': access_type if access_type is not None else 'private',
            'line_index': line_idx,
            'var_index': var_idx,
        }

    def get_method_data(self, lines, method_name):
        method_name = method_name.lower()
        for idx, line in enumerate(lines):
            lower_line = line.lower()

            if method_name in lower_line:
                method_data = self._extract_method_data(line, method_name, idx + 1)

                if method_data is None:
                    continue

                return method_data

        return None

    def _extract_method_data(self, line, name, line_idx):
        words = line.replace(';', '').split()

        name_idx = -1
        is_static = False
        access_type = None
        for idx, word in enumerate(words):
            if '(' in word:
                name_idx = idx
                continue

            if word == 'static':
                is_static = True
                continue

            if word in ['public', 'private', 'protected']:
                access_type = word
                continue

        if name_idx == -1:
            return None

        method_name = words[name_idx][:words[name_idx].index('(')]
        method_type = words[name_idx - 1]

        parenthesis_open = line.index('(')
        parenthesis_closed = line.index(')')
        method_params = [param.strip() for param in line[parenthesis_open + 1:parenthesis_closed].split(',')]

        method_idx = line.lower().index(name)
        return {
            'name': method_name,
            'type': method_type,
            'params': method_params if method_params != [''] else [],
            'static': is_static,
            'access_type': access_type if access_type is not None else 'private',
            'line_index': line_idx,
            'method_index': method_idx,
            'params_end_index': parenthesis_closed
        }

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

    def add_for_each(self, var_name, array_name):
        pass

    def add_for_loop(self, var_name, start, end):
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
