import keyboard

from prog_langs.base_prog_lang import BaseProgrammingLanguage

from utils import get_classes_in_module


class ProgrammingLanguageJava(BaseProgrammingLanguage):
    identifiers = ['java']
    name = 'Java'

    extensions = ['.java']

    requires_semicolon = True

    def create_class(self, name):
        code = f'public class {name} {{}}'
        self._write_code(code, False)

        return 1

    def create_method(self, name, access_type, is_static, ret_type):
        code = f'{access_type} '
        code += 'static ' if is_static else ''
        code += f'{ret_type} {name}() {{}}'
        self._write_code(code, False)

        return 1

    def create_variable(self, var_type, var_name):
        code = f'{var_type} {var_name}'
        self._write_code(code, True, False)

        return 0

    def set_variable(self, line, var_name, var_value):
        line_words = line.split()

        new_line = None
        for idx, word in enumerate(line_words):
            if word == f'{var_name};':
                new_line = line[:-1] + f' = {var_value}'
                break

            if word == '=':
                new_line = ' '.join(line_words[:idx + 1]) + f' {var_value}'
                break

        if new_line is None:
            print(f'Could not set variable {var_name} to {var_value}')
            return 0

        keyboard.press_and_release('ctrl+l')
        self._write_code(new_line, True)

        return 0

    def find_variable(self, lines, var_name):
        for idx, line in enumerate(lines):
            if var_name in line:
                line_words = line.split()

                # Must have type left of it
                if var_name in line_words[0]:
                    continue

                return idx + 1

        return -1


class ProgrammingLanguagePython(BaseProgrammingLanguage):
    identifiers = ['python', 'py']
    name = 'Python'

    extensions = ['.py']

    requires_semicolon = False


def get_prog_langs():
    return get_classes_in_module(__name__, subclass_of=BaseProgrammingLanguage)
