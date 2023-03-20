import platform

import reader

from editors.base_editor import BaseEditor, UnsupportedEditor
from editors.editors import get_editors

from platforms.base_platform import BasePlatform, UnsupportedPlatform
from platforms.platforms import get_platforms

from prog_langs.base_prog_lang import BaseProgrammingLanguage
from prog_langs.prog_langs import get_prog_langs

CONTEXT_SAVE_PATH = r'%LOCALAPPDATA%\Codetronaut\context.json'


class Context:
    _platform: BasePlatform
    _editor: BaseEditor
    _prog_lang: BaseProgrammingLanguage

    workdir: str = ''

    _editor_pid: int = -1

    _available_editors: list
    _available_langs: list

    def __init__(self):
        self._platform = None
        self._editor = None
        self._prog_lang = None

        self._get_platform()

        self._get_available_editors()
        self._get_available_langs()

    ##########################################
    #                 Internal               #
    ##########################################
    def save_config(self):
        config = {
            'workdir': self.workdir if self.workdir else '',
            'editor': self._editor.identifiers[0] if self._editor else '',
        }

        self._platform.write_to_file(CONTEXT_SAVE_PATH, config, to_json=True)

    def load_config(self):
        config = self._platform.read_from_file(CONTEXT_SAVE_PATH, is_json=True)

        if config['editor'] != '':
            self.set_editor(config['editor'])

        if config['workdir'] != '':
            self.set_workdir(config['workdir'])

    def clean_up(self):
        self.close_editor()

        self.save_config()

    def _get_platform(self):
        platform_class = None
        os_name = platform.system()

        platforms = get_platforms()
        for pf in platforms:
            if pf.identifier == os_name:
                platform_class = pf
                break

        if platform_class is None:
            raise UnsupportedPlatform(f'{os_name} is not a supported platform')

        self._platform = platform_class()

    def _get_available_editors(self):
        self._available_editors = get_editors()

    def _get_available_langs(self):
        self._available_langs = get_prog_langs()

    def set_workdir(self, path):
        self.workdir = path.replace('/', '\\')

        self.close_editor()
        self.start_editor()

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
        editor_class = None
        for editor in self._available_editors:
            if name in editor.identifiers:
                editor_class = editor
                break

        if editor_class is None:
            raise UnsupportedEditor(f'{name} is not a supported editor')

        self._editor = editor_class()
        reader.read_text(f'Editor set to {self._editor.name}')

    def is_valid_editor_name(self, name):
        for editor in self._available_editors:
            if name in editor.identifiers:
                return True

        return False

    def go_to_file(self, name):
        self._editor.go_to_file(name)

    ##########################################
    #               Prog Langs               #
    ##########################################
    def get_extension_by_prog_name(self, name):
        for lang in self._available_langs:
            if name in lang.identifiers:
                return lang.extensions[0]

        return None

    ##########################################
    #                 Platform               #
    ##########################################
    def get_files_in_directory(self, directory):
        return self._platform.get_files_in_directory(directory)

    def create_file(self, name):
        self._platform.create_file(name, root_dir=self.workdir)
