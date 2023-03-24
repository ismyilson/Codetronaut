import platform
import time

import reader

from editors.base_editor import BaseEditor, UnsupportedEditor
from editors.editors import get_editors

from platforms.base_platform import BasePlatform, UnsupportedPlatform
from platforms.platforms import get_platforms

from prog_langs.base_prog_lang import BaseProgrammingLanguage, UnsupportedProgrammingLanguage
from prog_langs.prog_langs import get_prog_langs

CONTEXT_SAVE_PATH = r'%LOCALAPPDATA%\Codetronaut\context.json'


class Context:
    _platform: BasePlatform
    _editor_: BaseEditor
    _prog_lang: BaseProgrammingLanguage

    workdir: str = ''

    _current_file: str = ''
    current_file_lines: list[str] = []

    current_line: int = 1

    _editor_pid: int = -1

    _available_editors: list
    _available_langs: list

    def __init__(self):
        self._platform = None
        self._editor_ = None
        self._prog_lang = None

        self._get_platform()

        self._get_available_editors()
        self._get_available_langs()

    ##########################################
    #                 Internal               #
    ##########################################
    @property
    def _editor(self):
        self._platform.focus(self._editor_pid)
        return self._editor_

    @_editor.setter
    def _editor(self, value):
        self._editor_ = value

    @property
    def current_file(self):
        return f'{self.workdir}{self._current_file}'

    @current_file.setter
    def current_file(self, value):
        self._current_file = value

    def save_config(self):
        config = {
            'workdir': self.workdir if self.workdir else '',
            'current_file': self._current_file if self._current_file else '',
            'editor': self._editor.identifiers[0] if self._editor else '',
            'current_line': self.current_line
        }

        self._platform.write_file(CONTEXT_SAVE_PATH, config, to_json=True)

    def load_config(self):
        config = self._platform.read_file(CONTEXT_SAVE_PATH, is_json=True)

        editor_name = config.get('editor', None)
        self.set_editor(editor_name)

        workdir = config.get('workdir', None)
        self.set_workdir(workdir)

        current_file = config.get('current_file', '')
        self.set_current_file(current_file)

        current_line = config.get('current_line', '')
        self.current_line = current_line

    def clean_up(self):
        self.save_all_files()
        self.save_open_file()

        self.save_config()

        self.close_editor()

    def _get_platform(self):
        platform_class = None
        os_name = platform.system()

        platforms = get_platforms()
        for pf in platforms:
            if pf.identifier == os_name:
                platform_class = pf
                break

        if platform_class is None:
            raise UnsupportedPlatform(f'"{os_name}" is not a supported platform')

        self._platform = platform_class()

    def _get_available_editors(self):
        self._available_editors = get_editors()

    def _get_available_langs(self):
        self._available_langs = get_prog_langs()

    def set_workdir(self, path):
        if path is None:
            return

        path = path.replace('/', '\\')
        if path[-1] != '\\':
            path += '\\'

        self.workdir = path

        self.close_editor()
        self.start_editor()

    def set_current_file(self, file):
        self.current_file = file
        self.current_line = 1

        self.current_file_lines = self._platform.get_file_lines(self.current_file)

        prog_lang_class = self.get_prog_lang_by_file_ext(file[file.rfind('.'):])

        if prog_lang_class is None:
            print(f'"{file}" is not part of a supported programming language')
            self._prog_lang = None
            return

        if type(self._prog_lang) is not prog_lang_class:
            self._prog_lang = prog_lang_class()

            print(f'Prog lang set to {self._prog_lang.name}')

    def save_open_file(self):
        self._editor.save_file()
        time.sleep(0.5)
        self.current_file_lines = self._platform.get_file_lines(self.current_file)

    def save_all_files(self):
        self._editor.save_all_files()
        time.sleep(0.5)
        self.current_file_lines = self._platform.get_file_lines(self.current_file)

    ##########################################
    #                 Editor                 #
    ##########################################
    def start_editor(self):
        if self._editor is None:
            return

        install_path = self._platform.get_install_path(self._editor.name)
        if install_path is None:
            print('Cant find editor path')
            return

        if self.workdir is None:
            process = self._platform.run(f'{install_path}\\{self._editor.exe_name}')
        else:
            process = self._platform.run(f'{install_path}\\{self._editor.exe_name}', '.', from_dir=f'{self.workdir}')

        self._editor_pid = process.pid

    def close_editor(self):
        if self._editor_pid == -1:
            return

        self._platform.close(self._editor_pid)
        self._editor_pid = -1

    def set_editor(self, name):
        if name is None:
            return

        editor_class = None
        for editor in self._available_editors:
            if name in editor.identifiers:
                editor_class = editor
                break

        if editor_class is None:
            raise UnsupportedEditor(f'"{name}" is not a supported editor')

        self._editor = editor_class()
        reader.read_text(f'Editor set to {self._editor.name}')

    def is_valid_editor_name(self, name):
        for editor in self._available_editors:
            if name in editor.identifiers:
                return True

        return False

    def go_to_file(self, name):
        self._editor.go_to_file(name)

        self.set_current_file(name)

    def go_to_line(self, line, column=None):
        if column:
            self._editor.go_to_line(line, column)
        else:
            self._editor.go_to_line(line)

        self.current_line = int(line)

    def go_to_variable(self, name):
        line, col = self._prog_lang.find_variable(self.current_file_lines, name)

        self.go_to_line(line, col)
        return line

    def go_to_next_available_line(self, create_line=True):
        line = self.next_available_line(create_line)

        if self.current_line != line:
            self.go_to_line(line)

    def next_available_line(self, create_line=True):
        if self.current_file_lines[self.current_line - 1].strip() == ''\
                or self.current_file_lines[self.current_line - 1].strip() == '\n':
            return self.current_line

        if create_line:
            self._editor.new_line()

        return self.current_line + 1

    def delete_lines(self, line_start, line_end):
        line_start = line_start if line_start else self.current_line
        line_end = line_end if line_end else self.current_line

        self.save_open_file()  # Save first
        self._platform.delete_lines_from_file(self.current_file, line_start, line_end)

    def rename_variable(self, var_name, new_var_name):
        self.go_to_variable(var_name)

        self._editor.refactor_rename(new_var_name)

    ##########################################
    #               Prog Langs               #
    ##########################################
    def get_extension_by_prog_name(self, name):
        for lang in self._available_langs:
            if name in lang.identifiers:
                return lang.extensions[0]

        return None

    def get_prog_lang_by_file_ext(self, ext):
        for lang in self._available_langs:
            if ext in lang.extensions:
                return lang

        return None

    def create_class(self, name):
        end_line = self._prog_lang.create_class(name)

        self.go_to_line(self.current_line + end_line)

        self.save_open_file()

    def create_method(self, name, access_type, is_static, ret_type):
        self.go_to_next_available_line()

        end_line = self._prog_lang.create_method(name, access_type, is_static, ret_type)

        self.go_to_line(self.current_line + end_line)

        self.save_open_file()

    def create_variable(self, var_type, var_name):
        self.go_to_next_available_line()

        end_line = self._prog_lang.create_variable(var_type, var_name)

        self.go_to_line(self.current_line + end_line)

        self.save_open_file()

    def set_variable_initial_value(self, var_name, var_value):
        line_idx = self.go_to_variable(var_name)
        line = self.current_file_lines[line_idx - 1]

        end_line = self._prog_lang.set_variable_initial_value(line, var_name, var_value)

        self.go_to_line(self.current_line + end_line)

        self.save_open_file()

    def set_variable(self, var_name, var_value):
        self.go_to_next_available_line()

        end_line = self._prog_lang.set_variable(var_name, var_value)

        self.save_open_file()

    def add_if_condition(self, first_part, operation, second_part):
        self.go_to_next_available_line()

        self._prog_lang.add_if_condition(first_part, operation, second_part)

    def add_return(self, value):
        self.go_to_next_available_line()

        self._prog_lang.add_return(value)

    ##########################################
    #                 Platform               #
    ##########################################
    def get_files_in_directory(self, directory):
        return self._platform.get_files_in_directory(directory)

    def create_file(self, name):
        self._platform.create_file(name, root_dir=self.workdir)

        time.sleep(1)  # Updating new files in IDEs and stuff requires bit of time

        self.go_to_file(name)

    def file_exists(self, name):
        return self._platform.file_exists(name, root_dir=self.workdir)

    def get_current_file_line_count(self):
        return len(self.current_file_lines)
